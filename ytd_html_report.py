from datetime import date

from database import Database
from py_html import PyHTML

def generate_report():
    """
    Generate an HTML report of YTD weekly attendance
    """
    report = PyHTML("YTD Attendance Report")
    db = Database()

    current_year: int = date.today().year
    start_week: str = str(current_year) + '-01'
    end_week: str = str(current_year) + "-" + str(date.today().isocalendar().week).zfill(2)

    weeks: list[tuple] = db.get_weekly_summary(start_week=start_week, end_week=end_week)
    ytd_average: float = db.get_ytd_average(year=current_year, end_week=end_week)
    current_week_count: int = db.get_weekly_count(week_number=end_week)
    db.close()

    report.h1("YTD Attendance Report")
    report.p(f"YTD average: {ytd_average:.2f}")
    report.p(f"Current week count: {current_week_count}")
    table_headers = ["Week #", "Start Date", "End Date", "Count"]
    report.table(table_headers, weeks)
    report.render("ytd_location_report.html")



if __name__ == "__main__":
    generate_report()
