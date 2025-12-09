import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import logging
import numpy as np

logger = logging.getLogger(__name__)

st.set_page_config(page_title="My Program", page_icon="🎯", layout="wide")
SideBarLinks()


BASE_URL = "http://web-api:4000"

st.markdown(
    """
    <style>
        :root {
            --fit-primary: #ff4d4f;
            --fit-secondary: #05d5ff;
            --fit-bg: #ffffff;
            --fit-card: rgba(0,0,0,0.02);
            --fit-stroke: rgba(0,0,0,0.08);
        }
        [data-testid="stAppViewContainer"] {
            background: var(--fit-bg);
            color: #0f172a;
        }
        .fit-card {
            border-radius: 14px;
            padding: 14px 16px;
            background: linear-gradient(160deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01));
            border: 1px solid var(--fit-stroke);
            box-shadow: 0 10px 28px rgba(0,0,0,0.18);
        }
        .fit-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            border-radius: 30px;
            border: 1px solid var(--fit-stroke);
            background: rgba(5,213,255,0.08);
            font-size: 0.9rem;
            color: #0f172a;
        }
        .fit-section {
            border-radius: 14px;
            border: 1px solid var(--fit-stroke);
            padding: 16px;
            background: #fff;
            box-shadow: 0 8px 22px rgba(0,0,0,0.12);
        }
        .stButton button, .stDownloadButton button {
            background: linear-gradient(135deg, var(--fit-primary), #ff6b6d);
            color: #fff;
            border: none;
            box-shadow: 0 10px 25px rgba(255,77,79,0.35);
        }
        .stButton button:hover, .stDownloadButton button:hover { transform: translateY(-1px); }
        .stSubheader, h1, h2, h3 { color: #0f172a; }
        .stMetric { background: rgba(0,0,0,0.01); border-radius: 12px; padding: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎯 My Training Program")
st.markdown(f"### {st.session_state.client_name}'s Coach-Assigned Workout Plan")
st.markdown("---")

try:
    response = requests.get(
        f"{BASE_URL}/client_specific_workout_program/exercises",
        params={"client_id": st.session_state.client_id},
        timeout=5
    )

    if response.status_code == 200:
        program_data = response.json()

        if not program_data:
            # No program assigned
            st.info("📋 No program assigned yet. Please contact your trainer to get a personalized workout program!")
            st.markdown("""
            ### What to expect:
            
            Your trainer will create a customized workout program based on:
            - Your fitness goals
            - Current fitness level
            - Available equipment
            - Time commitment
            
            Once assigned, your program will appear here with detailed exercise instructions.
            """)
        else:
            df = pd.DataFrame(program_data)

            # Ensure required columns from the route exist
            expected_cols = {
                "program_name",
                "workout_name",
                "workout_description",
                "duration_minutes",
                "difficulty",
                "exercise_name",
                "sets",
                "reps",
                "rest_period",
            }
            missing = expected_cols - set(df.columns)
            if missing:
                st.error(f"API did not return expected fields: {', '.join(missing)}")
                st.stop()

            # Convert numeric fields once
            df["sets"] = pd.to_numeric(df["sets"], errors="coerce")
            df["reps"] = pd.to_numeric(df["reps"], errors="coerce")
            df["rest_period"] = pd.to_numeric(df["rest_period"], errors="coerce")

            def display_num(val, suffix: str = ""):
                """Pretty-print numeric values, show '-' only when truly missing."""
                if pd.isna(val):
                    return "-" if not suffix else f"- {suffix}"
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                return f"{val}{suffix}"

            # Grab header info from first row (Chester has one current program)
            first = df.iloc[0]
            program_name = first["program_name"]
            workout_name = first["workout_name"]
            workout_description = first["workout_description"]
            duration = first["duration_minutes"]
            difficulty = first["difficulty"]

            # Top summary section
            col1, col2, col3 = st.columns([3, 1.5, 1.5])

            with col1:
                st.subheader(f"📋 Program: {program_name}")
                st.markdown(f"**Workout:** {workout_name}")
                if isinstance(workout_description, str) and workout_description.strip():
                    st.markdown(f"_{workout_description}_")

            with col2:
                st.metric("🕒 Duration", display_num(duration, " min"))
                st.metric("🔥 Difficulty", difficulty if difficulty else "-")

            with col3:
                st.metric("💪 Total Exercises", len(df))
                total_sets = df["sets"].sum()
                st.metric("🔢 Total Sets", display_num(total_sets))

            st.markdown("---")

            # Exercise details
            st.subheader("💪 Exercise Details")

            for idx, row in df.iterrows():
                ex_name = row["exercise_name"]
                sets_val = row["sets"]
                reps_val = row["reps"]
                rest_val = row["rest_period"]

                with st.expander(f"**{idx + 1}. {ex_name}**", expanded=True):
                    col_a, col_b, col_c, col_d = st.columns(4)

                    with col_a:
                        st.metric("🔢 Sets", display_num(sets_val))

                    with col_b:
                        st.metric("🔁 Reps", display_num(reps_val))

                    with col_c:
                        st.metric("⏱️ Rest", display_num(rest_val, "s"))

                    with col_d:
                        if not pd.isna(sets_val) and not pd.isna(rest_val):
                            total_time_min = sets_val * (rest_val / 60)
                        else:
                            total_time_min = np.nan
                        st.metric(
                            "⏰ Est. Time",
                            display_num(
                                round(total_time_min, 1) if not pd.isna(total_time_min) else np.nan,
                                "min",
                            ),
                        )

                    st.markdown(
                        f"""
                        **Workout Protocol:**
                        - Perform **{display_num(sets_val)} sets** of **{display_num(reps_val)} repetitions**
                        - Rest **{display_num(rest_val)} seconds** between sets  
                        - Focus on **control, breathing, and full range of motion**
                        """
                    )

            st.markdown("---")

            # Summary table
            st.subheader("📊 Program Summary")

            summary_df = df[["exercise_name", "sets", "reps", "rest_period"]].copy()
            summary_df["total_reps"] = (summary_df["sets"] * summary_df["reps"]).fillna(0).astype(int)
            summary_df["est_time_min"] = (
                (summary_df["sets"] * summary_df["rest_period"] / 60).fillna(0).round(1)
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "exercise_name": "Exercise",
                    "sets": "Sets",
                    "reps": "Reps",
                    "rest_period": "Rest (sec)",
                    "total_reps": "Total Reps",
                    "est_time_min": "Est. Time (min)",
                },
            )

            # Program statistics
            st.markdown("---")
            st.subheader("📈 Program Statistics")

            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

            with stat_col1:
                st.metric("Exercises", len(df))

            with stat_col2:
                st.metric("Total Sets", display_num(df["sets"].sum()))

            with stat_col3:
                st.metric("Total Reps", display_num((df["sets"] * df["reps"]).sum()))

            with stat_col4:
                est_duration = (df["sets"] * df["rest_period"]).sum() / 60
                st.metric("Est. Rest Time", display_num(round(est_duration, 1), "min"))

            st.markdown("---")

            # Export options
            st.subheader("📥 Export Program")
            col_export1, col_export2, col_export3 = st.columns([1, 1, 2])

            with col_export1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Download as CSV",
                    data=csv,
                    file_name=f"{program_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col_export2:
                printable = f"{program_name}\n{'=' * 50}\n\n"
                for _, row in df.iterrows():
                    printable += f"""
{row['exercise_name']}
- Sets: {display_num(row['sets'])}
- Reps: {display_num(row['reps'])}
- Rest: {display_num(row['rest_period'], 's')}

"""
                st.download_button(
                    label="📄 Download as TXT",
                    data=printable,
                    file_name=f"{program_name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            # Training tips
            st.markdown("---")
            st.subheader("💡 Training Tips")

            st.markdown(
                """
            - **Warm up properly** before starting your workout  
            - **Prioritize form** over heavy weight  
            - **Log each session** to track progression  
            - **Rest adequately** between workouts  
            - **Stay hydrated** throughout your session  
            - **Reach out to your trainer** if you are unsure about any exercise  
            """
            )

    elif response.status_code == 404:
        st.info("📋 No program assigned yet. Please contact your trainer to get a personalized workout program!")
        st.markdown("""
        ### What to expect:
        
        Your trainer will create a customized workout program based on:
        - Your fitness goals
        - Current fitness level
        - Available equipment
        - Time commitment
        
        Once assigned, your program will appear here with detailed exercise instructions.
        """)
    else:
        st.error(f"Failed to load program data (Status: {response.status_code})")

except Exception as e:
    st.error(f"Error connecting to API: {str(e)}")
    st.info("Make sure your Flask API is running in Docker as `web-api` on port 4000.")

st.markdown("---")

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("pages/21_Client_home.py")

with col2:
    if st.button("📊 View Dashboard", use_container_width=True):
        st.switch_page("pages/22_client_dashboard.py")

with col3:
    if st.button("📝 Log Workout", use_container_width=True):
        st.switch_page("pages/23_client_log_workout.py")

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>💪 FitFlow © 2025 | Questions about your program? Contact your trainer!</p>
</div>
""",
    unsafe_allow_html=True,
)
