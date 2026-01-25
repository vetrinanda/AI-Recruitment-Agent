from app.main import process_application


def main():
    application_text = "I have 10 years of experience in software development with expertise in Python."
    result = process_application(application_text)
    print("Final Result:", result)


if __name__ == "__main__":
    main()
