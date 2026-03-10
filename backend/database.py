import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kashyap@1100',
        database='job_agent'
    )
    

    return conn

def save_application(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO applications 
    (user_email, hr_email, name, phone, github_link, linkedin_link, job_description, email_body, status)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data.get("user_email"),
        data.get("email"),
        data.get("name"),
        data.get("phone"),
        data.get("github_link"),
        data.get("linkedin_link"),
        data.get("job_description"),
        data.get("email_body"),
        data.get("status")
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()