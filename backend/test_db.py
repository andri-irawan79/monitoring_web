"""Manual database connection check."""

def main():
    from database.connection import engine
    try:
        connection = engine.connect()
        print("Database Connected!")
        connection.close()
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
