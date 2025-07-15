from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
# Entry point to launch the app