from graphviz import Digraph

def create_mentiq_lifecycle():
    dot = Digraph(comment='MentIQ Website Lifecycle', format='png')
    dot.attr(rankdir='TB', size='10')

    # Styles
    dot.attr('node', shape='rect', style='filled', fontname='Helvetica')
    
    # Colors
    c_patient = '#E8F5E9'  # Light Green
    c_doctor = '#F3E5F5'   # Light Purple
    c_system = '#E1F5FE'   # Light Blue
    c_data = '#FFF9C4'     # Light Yellow

    # Nodes: Entry & Auth
    dot.node('Start', 'User Visits Homepage', fillcolor=c_system)
    dot.node('Auth', 'Login / Register', fillcolor=c_system, shape='diamond')

    # Nodes: Patient Journey
    dot.node('P_Dash', 'Patient Dashboard', fillcolor=c_patient)
    dot.node('Assess', 'Mental Health Assessment\n(Sleep, Anxiety, etc.)', fillcolor=c_patient)
    dot.node('Risk', 'AI Risk Model Output\n(At Risk / Low Risk)', fillcolor=c_data, shape='ellipse')
    dot.node('DocSearch', 'Find Doctors\n(Filter by Specialty)', fillcolor=c_patient)
    dot.node('Book', 'Book Appointment\n(Creates Pending Request)', fillcolor=c_data, shape='ellipse')

    # Nodes: Doctor Journey
    dot.node('D_Dash', 'Doctor Dashboard', fillcolor=c_doctor)
    dot.node('Manage', 'Manage Appointments\n(View Pending)', fillcolor=c_doctor)
    dot.node('Action', 'Confirm / Delete', fillcolor=c_doctor, shape='diamond')
    dot.node('Consult', 'Consultation Complete', fillcolor=c_doctor)

    # Nodes: Database
    dot.node('DB', 'SQLite Database\n(Users, Appts, History)', shape='cylinder', fillcolor='#EEEEEE')

    # Edges: Flow
    dot.edge('Start', 'Auth')
    dot.edge('Auth', 'P_Dash', label='Patient Login')
    dot.edge('Auth', 'D_Dash', label='Doctor Login')

    # Patient Flow
    dot.edge('P_Dash', 'Assess')
    dot.edge('Assess', 'Risk', label='Submit Data')
    dot.edge('Risk', 'DB', label='Save History')
    dot.edge('P_Dash', 'DocSearch')
    dot.edge('DocSearch', 'Book')
    dot.edge('Book', 'DB', label='Insert Pending')

    # Doctor Flow
    dot.edge('D_Dash', 'Manage')
    dot.edge('DB', 'Manage', label='Fetch Requests')
    dot.edge('Manage', 'Action')
    dot.edge('Action', 'DB', label='Update Status\n(Confirmed)')
    dot.edge('Action', 'Consult')
    dot.edge('Consult', 'DB', label='Update Status\n(Completed)')

    # Connection
    dot.edge('Book', 'Manage', style='dashed', label='Patient Request appears in Doctor View')

    # Render
    dot.render('mentiq_lifecycle_graph', view=True)
    print("Graph generated as mentiq_lifecycle_graph.png")

if __name__ == '__main__':
    create_mentiq_lifecycle()