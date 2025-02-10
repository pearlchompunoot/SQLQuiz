import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import random
import dash_bootstrap_components as dbc

# Question and Answer Data (same as your Tkinter app)
question = {
    "What does 'SQL' stand for?":
        ['STRUCTURED QUERY LANGUAGE', 'STANDARD QUERY LANGUAGE', 'STRONG QUERY LANGUAGE', 'STANDARDIZED QUESTION LANGUAGE'],
    "Which is the correct order of execution in SQL? ":
        ["SELECT > FROM > WHERE > LIMIT > GROUP BY > HAVING", "FROM > WHERE > GROUP BY > HAVING > LIMIT", "WHERE > LIMIT > GROUP BY > FROM > SELECT", "FROM > HAVING > GROUP BY > WHERE > LIMIT"],
    "Which is the correct query for retrieving TOP 5 Japan spenders' name and amount of spending? ":
        ["SELECT  customer_name, spending  FROM customers where country = 'Japan' LIMIT 5;",
         "SELECT  customer_name, spending  FROM customers where country = 'Japan' LIMIT 5 ORDER BY spending;",
         "SELECT customer_name, spending FROM customers where country = 'Japan' GROUP BY customer_name ORDER BY spending LIMIT 5;",
         "SELECT customer_name, spending FROM customers where country = 'Japan' GROUP BY customer_name ORDER BY spending DESC LIMIT 5;"],
    "Which statement is incorrect about a Primary key and a Foreign key?":
        ["A Primary key is the unique identifier within it table.",
         "Foreign keys are always Primary keys.",
         "A Foreign key is a field that refers to a primary key in another table.",
         "A table can have only one Primary key. "],
    "How do you select all the records from a table named 'customers' where the value of the column 'customer_name' starts with 'F' ?":
        ["SELECT * FROM customers WHERE customer_name = 'F';",
         "SELECT * FROM customers WHERE customer_name LIKE 'F';",
         "SELECT * FROM customers WHERE customer_name LIKE 'F%';",
         "SELECT * FROM customers WHERE customer_name IS 'F%';"] ,
    "What is the most appropriate approach to deal with NULL value?":
        ["Use 'COALESCE' to set all Null value as zero straightaway.",
         "Understand why the NULL values appeared, before deciding how to deal with it.", "Remove all rows that contain NULL value straightaway.",
         "Completely ignore the null values."],
    "How do you select all the records from a table named 'customers' where the column 'country' is 'UK' and the column 'spending' is less than 1000? ":
        ["SELECT * FROM customers WHERE country = 'UK' AND spending < 1000;",
         "SELECT * FROM customers WHERE country = 'UK' , spending < 1000;",
         "SELECT * FROM customers HAVING country = 'UK' AND spending < 1000;",
         "SELECT * FROM customers HAVING country = 'UK' + spending < 1000;"],
    "Which SQL statement is used to remove records from a database table?":
        ["SELECT", "INSERT", "UPDATE", "DELETE"],
    "How do you get the number of customers from each country?":
        ["SELECT country, COUNT(*) FROM customers GROUP BY country;",
         "SELECT country, COUNT DISTINCT (*) FROM customers GROUP BY country;",
         "SELECT country, COUNT (*) FROM customers GROUP BY country;",
         "SELECT DISTINCT country, SUM(*) FROM customers GROUP BY country;"],
    "How can you return the number of records in the 'customers' table?":
        ["SELECT * FROM customers;",
         "SELECT COUNT(*) FROM customers;",
         "SELECT LEN(*) FROM customers;",
         "SELECT NUMBER(*) FROM customers;"],
    "Which SQL aggregate function returns the average value of a numeric column?":
        ["SUM()", "AVG()", "COUNT()", "MAX()"],
    "Which SQL aggregate function returns the sum of values in a numeric column?":
        ["SUM()", "AVG()", "COUNT()", "MAX()"],
    "Which SQL aggregate function returns the largest value in a set of values?":
        ["SUM()", "AVG()", "COUNT()", "MAX()"],
    "Which SQL clause is used to group rows that have the same values in specified columns into summary rows?":
        ["ORDER BY", "GROUP BY", "WHERE", "HAVING"],
    "Which SQL clause is used to filter groups based on a specified condition?":
        ["ORDER BY", "GROUP BY", "WHERE", "HAVING"],
    "Which type of JOIN returns rows when there is a match in both tables?":
        ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL OUTER JOIN"],
    "Which type of JOIN returns all rows from the left table, and the matching rows from the right table?":
        ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL OUTER JOIN"],
    "How can you delete the records where the column 'customer_name' is 'Anna' in the customers Table?":
        ["DELETE FROM customers WHERE customer_name = 'Anna';",
         "REMOVE FROM customers WHERE customer_name = 'Anna';",
         "DELETE WHERE customer_name = 'Anna' FROM customers;",
         "DELETE customer_name = 'Anna' FROM customers;"],
    "How do you delete a table 'customers'?":
        ["DROP TABLE customers;",
         "DELETE TABLE customers;",
         "DELETE customers TABLE;",
         "DROP customers TABLE;"],
    "What does the SQL CASE expression do?":
        ["It iterates over table rows and returns a value for each column.",
         "It evaluates conditions and returns a value based on the first true condition.",
         "It combines rows from tables based on a condition.",
         "It selects the record from the table based on the condition."],
    "Which SQL constraint uniquely identifies each record in a table?":
        ["NOT NULL", "UNIQUE", "PRIMARY KEY", "FOREIGN KEY"],
    "Which SQL clause is used to limit the number of rows returned by a query?":
        ["ORDER BY", "GROUP BY", "WHERE", "LIMIT"],
    "What is a subquery?":
        ["A short query.", "A query nested inside another query.", "A query that updates data.", "A query that defines table structure."]
}
ans = [
    'STRUCTURED QUERY LANGUAGE',
    "FROM > WHERE > GROUP BY > HAVING > LIMIT",
    "SELECT customer_name, spending FROM customers where country = 'Japan' GROUP BY customer_name ORDER BY spending DESC LIMIT 5;",
    "Foreign keys are always Primary keys.",
    "SELECT * FROM customers WHERE customer_name LIKE 'F%';",
    "Understand why the NULL values appeared, before deciding how to deal with it.",
    "SELECT * FROM customers WHERE country = 'UK' AND spending < 1000;",
    "DELETE",
    "SELECT country, COUNT(*) FROM customers GROUP BY country;",
    "SELECT COUNT(*) FROM customers;",
    "AVG()",
    "SUM()",
    "MAX()",
    "GROUP BY",
    "HAVING",
    "INNER JOIN",
    "LEFT JOIN",
    "DELETE FROM customers WHERE customer_name = 'Anna';",
    "DROP TABLE customers;",
    "It evaluates conditions and returns a value based on the first true condition.",
    "PRIMARY KEY",
    "LIMIT",
    "A query nested inside another query."
] 

# Initialize Dash App
app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL],suppress_callback_exceptions=True)
app.title = "SQL Quiz"

server = app.server
# App Layout
app.layout = html.Div(
    style={'backgroundColor': 'rgba(168, 212, 247)', 'padding': '100px', 'fontFamily': 'Verdana'}, children=[
    html.H1("SQL Quiz", style={'textAlign': 'center', 'fontSize': '45px'}),
    html.Div(id='question-container', style={'color': 'black', 'fontSize': '22px', 'marginBottom': '20px'}),
    dcc.RadioItems(
        id='answer-options',
        options=[],
        value=None,
        labelStyle={'display': 'block'},
        style={'color': 'black', 'fontSize': '18px', 'marginBottom': '20px'}
    ),
    html.Div(id='feedback-message', style={'color': 'forest green', 'fontSize': '18px', 'marginBottom': '20px', 'fontStyle': 'italic'}),
    html.Button('Next Question', id='next-button', n_clicks=0, style={'fontSize': '18px', 
                                                                      'padding': '10px 20px', 
                                                                      'backgroundColor': 'white', 
                                                                      'color': 'sea green', 
                                                                      'border': 'none', 'borderRadius': '5px', 
                                                                      'cursor': 'pointer'}),
    html.Div(id='results-area', style={'color': 'black', 'fontSize': '25px', 'textAlign': 'center', 'marginTop': '30px'}, hidden=True),
    dcc.Store(id='current-question-index', data=0),
    dcc.Store(id='user-score', data=0),
    dcc.Store(id='shuffled-questions', data=[]),
    dcc.Store(id='answer-submitted', data=False)
])

@app.callback(
    [Output('question-container', 'children'),
     Output('answer-options', 'options'),
     Output('feedback-message', 'children'),
     Output('results-area', 'hidden'),
     Output('next-button', 'hidden'),
     Output('current-question-index', 'data'),
     Output('user-score', 'data'),
     Output('shuffled-questions', 'data'),
     Output('answer-submitted', 'data')],
    [Input('next-button', 'n_clicks'),
     Input('answer-options', 'value')],
    [State('current-question-index', 'data'),
     State('shuffled-questions', 'data'),
     State('user-score', 'data'),
     State('answer-submitted', 'data')]
)
def update_quiz(n_clicks, selected_answer, question_index, shuffled_questions, user_score, answer_submitted):
    ctx = dash.callback_context
    initializing_quiz = not ctx.triggered
    next_button_clicked = ctx.triggered[0]['prop_id'].split('.')[0] == 'next-button' if ctx.triggered else False
    answer_selected = ctx.triggered[0]['prop_id'].split('.')[0] == 'answer-options' if ctx.triggered else False

    # Initial quiz setup
    if initializing_quiz or not shuffled_questions:
        questions_list = list(question.keys())
        random.shuffle(questions_list)
        return f"Question 1: {questions_list[0]}", [{'label': opt, 'value': opt} for opt in question[questions_list[0]]], "", True, True, 0, 0, questions_list, False

    # End of quiz
    if question_index >= len(shuffled_questions):
        return f"Quiz Completed! Your Score: {user_score} out of {len(question)}", [], "", False, True, question_index, user_score, shuffled_questions, False

    # Get current question details
    current_question = shuffled_questions[question_index]
    options_list = question[current_question]
    correct_answer = ans[list(question.keys()).index(current_question)]

    feedback = ""
    updated_score = user_score
    updated_answer_submitted = answer_submitted
    updated_question_index = question_index

    # Answer selected
    if answer_selected and not answer_submitted:
        updated_answer_submitted = True
        if selected_answer == correct_answer:
            feedback = "✅ Correct!"
            updated_score += 1
        else:
            feedback = f"❌ Incorrect. The correct answer is: {correct_answer}"

    # Next question
    if next_button_clicked:
        updated_question_index += 1
        updated_answer_submitted = False
        if updated_question_index < len(shuffled_questions):
            return (f"Question {updated_question_index + 1}: {shuffled_questions[updated_question_index]}",
                    [{'label': opt, 'value': opt} for opt in question[shuffled_questions[updated_question_index]]], 
                    "", True, False, updated_question_index, updated_score, shuffled_questions, False)
        else:
            return f"Quiz Completed! Your Score: {updated_score} out of {len(question)}", [], "", False, True, updated_question_index, updated_score, shuffled_questions, False

    return (f"Question {question_index + 1}: {current_question}",
            [{'label': opt, 'value': opt} for opt in options_list], feedback, True, False, updated_question_index, updated_score, shuffled_questions, updated_answer_submitted)

if __name__ == '__main__':
    app.run_server(debug=True)
