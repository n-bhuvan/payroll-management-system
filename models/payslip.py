import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from models.payroll import calculate_net_salary


def generate_payslip(employee):

    employee_id = employee[0]
    name = employee[1]
    department = employee[2]
    position = employee[3]
    salary = employee[4]
    bonus = employee[5]
    deductions = employee[6]

    net_salary = calculate_net_salary(
        salary,
        bonus,
        deductions
    )

    os.makedirs("payslips", exist_ok=True)

    file_name = os.path.join(
        "payslips",
        f"Payslip_{employee_id}.pdf"
    )
    
    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Employee Payslip",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    details = f'''
    <b>Employee ID:</b> {employee_id}<br/>
    <b>Name:</b> {name}<br/>
    <b>Department:</b> {department}<br/>
    <b>Position:</b> {position}<br/>
    <b>Salary:</b> ₹{salary}<br/>
    <b>Bonus:</b> ₹{bonus}<br/>
    <b>Deductions:</b> ₹{deductions}<br/>
    <b>Net Salary:</b> ₹{net_salary}
    '''

    detail_paragraph = Paragraph(
        details,
        styles['BodyText']
    )

    elements.append(detail_paragraph)

    pdf.build(elements)

    return file_name