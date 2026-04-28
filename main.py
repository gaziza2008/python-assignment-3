import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")

        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True

        print(f"Error: {self.filename} not found. Please download the file from LMS.")
        return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")

        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")

        try:
            with open(self.filename, mode="r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                self.students = list(reader)

            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
            self.students = []
            return self.students

        except Exception as error:
            print(f"Error while loading data: {error}")
            self.students = []
            return self.students

    def preview(self, n=5):
        print(f"First {n} rows:")
        print("-" * 30)

        for student in self.students[:n]:
            print(
                f"{student['student_id']} | "
                f"{student['age']} | "
                f"{student['gender']} | "
                f"{student['country']} | "
                f"GPA: {student['GPA']}"
            )

        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        valid_students = []

        for student in self.students:
            try:
                float(student["final_exam_score"])
                float(student["GPA"])
                valid_students.append(student)
            except ValueError:
                print(
                    f"Warning: could not convert value for student "
                    f"{student.get('student_id', 'Unknown')} — skipping row."
                )
            except KeyError as error:
                print(
                    f"Warning: missing column {error} for student "
                    f"{student.get('student_id', 'Unknown')} — skipping row."
                )

        sorted_students = sorted(
            valid_students,
            key=lambda s: float(s["final_exam_score"]),
            reverse=True
        )

        top10 = sorted_students[:10]
        top10_result = []

        for i in range(len(top10)):
            student = top10[i]

            top10_result.append({
                "rank": i + 1,
                "student_id": student["student_id"],
                "country": student["country"],
                "major": student["major"],
                "final_exam_score": float(student["final_exam_score"]),
                "GPA": float(student["GPA"])
            })

        self.result = {
            "analysis": "Top 10 Students by Exam Score",
            "total_students": len(self.students),
            "top_10": top10_result
        }

        return self.result

    def print_results(self):
        print("-" * 30)
        print("Top 10 Students by Exam Score")
        print("-" * 30)

        for student in self.result["top_10"]:
            print(
                f"{student['rank']}. "
                f"{student['student_id']} | "
                f"{student['country']} | "
                f"{student['major']} | "
                f"Score: {student['final_exam_score']} | "
                f"GPA: {student['GPA']}"
            )

        print("-" * 30)
        print("=" * 30)
        print("ANALYSIS RESULT")
        print("=" * 30)
        print(f"Analysis : {self.result['analysis']}")
        print(f"Total students : {self.result['total_students']}")
        print("Top 10 saved to output/result.json")
        print("=" * 30)

    def show_lambda_filter_results(self):
        print("-" * 30)
        print("Lambda / Map / Filter")
        print("-" * 30)

        try:
            top_scorers = list(
                filter(lambda s: float(s["final_exam_score"]) > 95, self.students)
            )

            gpa_values = list(
                map(lambda s: float(s["GPA"]), self.students)
            )

            good_assignments = list(
                filter(lambda s: float(s["assignment_score"]) > 90, self.students)
            )

            print(f"Students with score > 95 : {len(top_scorers)}")
            print(f"GPA values (first 5) : {gpa_values[:5]}")
            print(f"Students assignment > 90 : {len(good_assignments)}")

        except ValueError:
            print("Warning: one or more numeric values could not be converted.")
        except KeyError as error:
            print(f"Warning: missing column {error}.")

        print("-" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, mode="w", encoding="utf-8") as file:
                json.dump(self.result, file, indent=4)

            print(f"Result saved to {self.output_path}")

        except Exception as error:
            print(f"Error while saving result: {error}")


def main():
    filename = "students.csv"
    output_folder = "output"
    output_path = os.path.join(output_folder, "result.json")

    file_manager = FileManager(filename)

    if not file_manager.check_file():
        print("Stopping program.")
        return

    file_manager.create_output_folder(output_folder)

    data_loader = DataLoader(filename)
    students = data_loader.load()

    if not students:
        print("No data loaded. Stopping program.")
        return

    data_loader.preview()

    analyser = DataAnalyser(students)
    analyser.analyse()
    analyser.print_results()
    analyser.show_lambda_filter_results()

    saver = ResultSaver(analyser.result, output_path)
    saver.save_json()


if __name__ == "__main__":
    main()
