from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Attendance

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
  # Example stats
  total_attendance = Attendance.query.filter_by(user_id=current_user.id).count()
  late_arrivals = Attendance.query.filter_by(user_id=current_user.id, is_late=True).count()

  return jsonify({
      'total_attendance': total_attendance,
      'late_arrivals': late_arrivals,
      'user': current_user.username
  })