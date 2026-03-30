from math import ceil
from datetime import datetime, timedelta

from flask import Flask, request, jsonify

default_duration = 15
default_max_duration_minutes = 60


def find_contigous_open_slots(n: int):
    """returns all the starting points that satisfy the constraint of having 'n' contigous 1's both in the morning and in the afternoon time_slots
       0 represents the slot is booked
       1 represents the slot is open and available for booking
       both in the morning_timeslots and the afternoon_timeslots lists.
    """
    morning_timeslots = [0 if i%7 == 0 else 1 for i in range(12)]
    afternoon_timeslots = [0 if i%7 == 0 else 1 for i in range(16)]
    print(f"morning_timeslots: {morning_timeslots}")
    print(f"evening_timeslots: {afternoon_timeslots}")
    
    def contiguous_blocks(timeslots_list: list[int]) -> list[int]:
        available_starts = []
        for i in range(len(timeslots_list) - n + 1):
            if all(timeslots_list[i + j] == 1 for j in range(n)):
                available_starts.append(i)
    
        return available_starts
    
    morning_availability = contiguous_blocks(morning_timeslots)
    afternoon_availability = contiguous_blocks(afternoon_timeslots)
    
    return morning_availability, afternoon_availability
    

def get_dates_around(date_str: str) -> list[str]:
    """
    outputs available appointment slots for a week around that date_str argument
    """
    today = datetime.today().date()
    user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    if user_date < today:
        return []
    
    if user_date > today + timedelta(days=365):
        return []
    
    left = user_date - timedelta(days=3)
    right = user_date + timedelta(days=3)
    
    if left < today:
        shift = (today - left).days
        left = today
        right += timedelta(days=shift)
    
    result = []
    current = left
    
    while len(result) < 7:
        if current.weekday() != 6:
            result.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    return result

def find_available_slots(date_requested, duration_requested_minutes):
    contigous_slots_required = ceil(duration_requested_minutes/default_duration)
    if contigous_slots_required > 4:
        return []
    
    def compute_available_slots():     
        m_slots_i, a_slots_i = find_contigous_open_slots(contigous_slots_required)

        # convert the integers to the clock time
        m_slots, a_slots = [], []
    
        for index in m_slots_i:
            start_hrs = 10 + (index * default_duration)//60
            start_mins = (index * default_duration)%60
            end_hrs = start_hrs + (duration_requested_minutes)//60
            end_mins = start_mins + (duration_requested_minutes)%60
            carry = end_mins//60
            end_hrs += carry
            end_mins = end_mins%60
            m_slots.append((start_hrs, start_mins, end_hrs, end_mins))

        for index in a_slots_i:
            start_hrs = 14 + (index * default_duration)//60
            start_mins = (index * default_duration)%60
            end_hrs = start_hrs + (duration_requested_minutes)//60
            end_mins = start_mins + (duration_requested_minutes)%60
            carry = end_mins//60
            end_hrs += carry
            end_mins = end_mins%60
            a_slots.append((start_hrs, start_mins, end_hrs, end_mins))

        return m_slots, a_slots
    
    week_around_requested_date = get_dates_around(date_requested)
    available_time_slots = {}
    for d in week_around_requested_date:
        m_slots, a_slots = compute_available_slots()
        available_time_slots[d] = {"morning_shift": m_slots, "afternoon_shift": a_slots}
    
    return available_time_slots


app = Flask(__name__)

@app.route("/availableslots", methods=["POST"])
def get_available_slots():
    req_data = request.get_json()
    date_requested = req_data.get("date_requested")
    available_timeslots = find_available_slots(req_data.get("date_requested"), req_data.get("duration_requested_minutes"))
    ats = []
    for d, v in available_timeslots.items():
        m_slots = v['morning_shift']
        for ts in m_slots:
            start_minutes = "00" if ts[1] == 0 else ts[1]
            end_minutes = "00" if ts[3] == 0 else ts[3]
            ats.append(f"{d}\n{ts[0]}:{start_minutes}-{ts[2]}:{end_minutes}")
        a_slots = v['afternoon_shift']
        for ts in a_slots:
            start_minutes = "00" if ts[1] == 0 else ts[1]
            end_minutes = "00" if ts[3] == 0 else ts[3]
            ats.append(f"{d}\n{ts[0]}:{start_minutes}-{ts[2]}:{end_minutes}")
    
    return jsonify({
        "available_timeslots": ats
    })

@app.route("/bookappointment", methods=["POST"])
def book_appointment():
    req_data = request.get_json()
    # requested_appointment_slot = req_data.get("requested_appointment_slot")
    d = req_data['date']
    ts = req_data['time_slot']
    return jsonify({
        "message": f"booking on {d} for {ts} is confirmed"
    })


if __name__ == "__main__":
    # date_requested = "2026-04-04"
    # duration_requested_minutes = 30
    # print(find_available_slots(date_requested, duration_requested_minutes))
    app.run(host="0.0.0.0", port=8000, debug=True)