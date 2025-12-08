from app import create_hospital_app

app = create_hospital_app()


if __name__ == "__main__":
    # Debug only for development
    app.run(debug=True)
