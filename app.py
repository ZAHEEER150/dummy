import streamlit as st
import mysql.connector
import pandas as pd


# ---------------- DATABASE CONNECTION ---------------- #

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="FITNESS_LOGGER"
    )


# ---------------- PAGE CONFIGURATION ---------------- #

st.set_page_config(
    page_title="Fitness Logger",
    page_icon="💪",
    layout="wide"
)

st.header("💪 FITNESS LOGGER")

st.sidebar.header("MODES")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["LOGGER", "ANALYTICS", "PREDICTOR"]
)


# ---------------- EXERCISE LIST ---------------- #

exercises = [
    "Incline Bench Press",
    "Incline Dumbell Press",
    "Cable Chest Fly",
    "Pec Dec",
    "Bench Press",
    "Machine Lateral Raises",
    "Dumbell Lateral Raises",
    "Cable Lateral Raises",
    "Dumbell Shoulder Press",
    "Machine Shoulder Press",
    "Lat Pulldown",
    "Assisted Pull-Up",
    "Weighted Pull-Up",
    "T-Bar Rows",
    "Close-Grip Row",
    "Horizontal Row",
    "Seated Cable Row",
    "Incline Curl",
    "Preacher Curl",
    "Bicep Curl",
    "Bayesian Curl",
    "Triceps Pushdown",
    "Tricep Overhead Extension",
    "Squat",
    "Leg Press",
    "Romanian Deadlift",
    "Leg Curl",
    "Calf Raises"
]

muscles = [
    "Chest",
    "Back",
    "Shoulders",
    "Biceps",
    "Triceps",
    "Quads",
    "Hamstrings",
    "Glutes",
    "Calves",
    "Abs"
]


# ==================== LOGGER ==================== #

if mode == "LOGGER":

    st.subheader("LOGGER")

    with st.form("workout_form"):

        exercise = st.selectbox(
            "Select Exercise",
            exercises
        )

        muscle = st.selectbox(
            "Select Muscle",
            muscles
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            metric = st.selectbox(
                "Select Metric",
                ["KG", "lbs"]
            )

        with col2:
            weight = st.number_input(
                "Enter Weight",
                min_value=0.0,
                step=0.5
            )

        with col3:
            reps = st.number_input(
                "Enter Reps",
                min_value=0,
                step=1
            )

        with col4:
            sets = st.number_input(
                "Enter Sets",
                min_value=0,
                step=1
            )

        submitted = st.form_submit_button(
            "Save Workout"
        )

        if submitted:

            if weight > 0 and reps > 0 and sets > 0:

                conn = None
                cursor = None

                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    query = """
                        INSERT INTO workouts
                        (exercise, muscle, metric, weight, reps, sets)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    values = (
                        exercise,
                        muscle,
                        metric,
                        weight,
                        reps,
                        sets
                    )

                    cursor.execute(query, values)
                    conn.commit()

                    st.success(
                        "Workout saved successfully!"
                    )

                except mysql.connector.Error as error:
                    st.error(
                        f"Database error: {error}"
                    )

                finally:
                    if cursor is not None:
                        cursor.close()

                    if conn is not None and conn.is_connected():
                        conn.close()

            else:
                st.warning(
                    "Weight, reps, and sets must be greater than zero."
                )


# ==================== ANALYTICS ==================== #

elif mode == "ANALYTICS":

    st.title("Workout Analytics")

    conn = None
    df = pd.DataFrame()

    try:
        conn = get_connection()

        query = """
            SELECT
                workout_date,
                exercise,
                muscle,
                metric,
                weight,
                reps,
                sets
            FROM workouts
            ORDER BY workout_date
        """

        df = pd.read_sql(
            query,
            conn
        )

    except mysql.connector.Error as error:
        st.error(
            f"Database error: {error}"
        )

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

    if not df.empty:

        # Exercise selection

        exercise = st.selectbox(
            "Select Exercise",
            sorted(df["exercise"].unique())
        )

        # Filter data for selected exercise

        exercise_df = df[
            df["exercise"] == exercise
        ].copy()

        exercise_df["workout_date"] = pd.to_datetime(
            exercise_df["workout_date"]
        )

        exercise_df = exercise_df.sort_values(
            "workout_date"
        )

        # Progress graph

        st.subheader(
            f"{exercise} — Progress Over Time"
        )

        st.line_chart(
            exercise_df.set_index("workout_date")["weight"]
        )

        # Workout history

        st.subheader("Workout History")

        st.dataframe(
            exercise_df[
                [
                    "workout_date",
                    "weight",
                    "metric",
                    "reps",
                    "sets"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        # Total workout statistics

        st.subheader("Exercise Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Workouts",
                len(exercise_df)
            )

        with col2:
            st.metric(
                "Best Recorded Weight",
                f"{exercise_df['weight'].max():g}"
            )

        with col3:
            st.metric(
                "Total Sets",
                int(exercise_df["sets"].sum())
            )

    else:
        st.info(
            "No workout data recorded yet. "
            "Log a workout first to see your analytics."
        )


# ==================== PREDICTOR ==================== #

elif mode == "PREDICTOR":

    st.subheader("إِنْ شَاءَ اللَّهُ")

    st.write("COMING SOON")