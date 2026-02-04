from datetime import datetime, timedelta

# waiting time in minutes (example)
waiting_time = st.session_state.wait_time

# current system time
current_time = datetime.now()

# expected turn time = current time + waiting time
expected_turn_time = current_time + timedelta(minutes=waiting_time)

# format in AM/PM
st.session_state.expected_time = expected_turn_time.strftime("%I:%M %p")
