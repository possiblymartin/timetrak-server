from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from app.models import Attendance, WorkSchedule
from app.dashboard import dashboard_bp
from app import db

# Total Employees Present
@dashboard_bp.route('/total_employees_present', methods=['GET'])
def total_employees_present():
    today_date = datetime.now().date()
    present_count = Attendance.query.filter(
        Attendance.attendance_date == today_date,
        Attendance.clock_in_time.isnot(None)
    ).count()
    return jsonify({"present_employees": present_count})

# Combined Metrics Endpoint
@dashboard_bp.route('/metrics', methods=['GET'])
def metrics():
    today_date = datetime.utcnow().date()

    try:
        # Total Employees Present
        present_count = Attendance.query.filter(
            Attendance.attendance_date == today_date,
            Attendance.clock_in_time.isnot(None)
        ).count()

        # Late Arrivals Count
        late_count = db.session.query(Attendance).join(WorkSchedule, Attendance.user_id == WorkSchedule.user_id).filter(
            Attendance.attendance_date == today_date,
            Attendance.clock_in_time > WorkSchedule.work_start_time
        ).count()

        # Average Clock-In Time
        avg_clock_in_time_seconds = db.session.query(
            func.avg(
              func.strftime('%H', Attendance.clock_in_time) * 3600 +
              func.strftime('%M', Attendance.clock_in_time) * 60 +
              func.strftime('%S', Attendance.clock_in_time)
            )
        ).filter(Attendance.attendance_date == today_date).scalar()

        avg_clock_in_time_formatted = None
        if avg_clock_in_time_seconds:
            avg_clock_in_time_formatted = str(timedelta(seconds=int(avg_clock_in_time_seconds)))

        return jsonify({
            "present_employees": present_count,
            "late_arrivals": late_count,
            "avg_clock_in_time": avg_clock_in_time_formatted,
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
