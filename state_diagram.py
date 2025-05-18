import graphviz

def generate_state_diagram():
    # Create a new directed graph
    dot = graphviz.Digraph(comment='BBQ Nation Chatbot State Machine')
    
    # Define states
    states = [
        "start", "collect_city", "collect_location_bangalore", "collect_location_delhi",
        "main_options", "new_booking", "collect_date", "collect_time", "collect_guests",
        "collect_phone", "booking_confirmation", "booking_complete", "modify_booking",
        "verify_reference", "modification_options", "cancel_booking", "cancellation_complete",
        "knowledge_query", "knowledge_response", "feedback", "collect_ratings",
        "collect_comments", "feedback_complete", "end"
    ]
    
    # Add states to the graph
    for state in states:
        dot.node(state)
    
    # Define transitions
    transitions = [
        ("start", "collect_city", "1-2"),
        ("start", "knowledge_query", "3"),
        ("start", "feedback", "4"),
        ("collect_city", "collect_location_bangalore", "1"),
        ("collect_city", "collect_location_delhi", "2"),
        ("collect_city", "start", "back"),
        ("collect_location_bangalore", "main_options", "1-4"),
        ("collect_location_bangalore", "collect_city", "back"),
        ("collect_location_delhi", "main_options", "1-3"),
        ("collect_location_delhi", "collect_city", "back"),
        ("main_options", "new_booking", "1"),
        ("main_options", "modify_booking", "2"),
        ("main_options", "knowledge_query", "3"),
        ("main_options", "feedback", "4"),
        ("main_options", "collect_city", "back"),
        ("new_booking", "collect_date", "next"),
        ("new_booking", "main_options", "back"),
        ("collect_date", "collect_time", "valid date"),
        ("collect_date", "new_booking", "back"),
        ("collect_time", "collect_guests", "1-2"),
        ("collect_time", "collect_date", "back"),
        ("collect_guests", "collect_phone", "valid number"),
        ("collect_guests", "collect_time", "back"),
        ("collect_phone", "booking_confirmation", "valid phone"),
        ("collect_phone", "collect_guests", "back"),
        ("booking_confirmation", "booking_complete", "1"),
        ("booking_confirmation", "new_booking", "2"),
        ("booking_confirmation", "collect_phone", "back"),
        ("booking_complete", "start", "1"),
        ("booking_complete", "end", "2"),
        ("modify_booking", "verify_reference", "next"),
        ("modify_booking", "main_options", "back"),
        ("verify_reference", "modification_options", "valid reference"),
        ("verify_reference", "modify_booking", "back"),
        ("modification_options", "collect_date", "1"),
        ("modification_options", "collect_time", "2"),
        ("modification_options", "collect_guests", "3"),
        ("modification_options", "cancel_booking", "4"),
        ("modification_options", "verify_reference", "back"),
        ("cancel_booking", "cancellation_complete", "1"),
        ("cancel_booking", "modification_options", "2"),
        ("cancel_booking", "modification_options", "back"),
        ("cancellation_complete", "start", "1"),
        ("cancellation_complete", "end", "2"),
        ("knowledge_query", "knowledge_response", "question"),
        ("knowledge_query", "main_options", "back"),
        ("knowledge_response", "knowledge_query", "1"),
        ("knowledge_response", "main_options", "2"),
        ("knowledge_response", "knowledge_query", "back"),
        ("feedback", "collect_ratings", "next"),
        ("feedback", "main_options", "back"),
        ("collect_ratings", "collect_comments", "valid rating"),
        ("collect_ratings", "feedback", "back"),
        ("collect_comments", "feedback_complete", "next"),
        ("collect_comments", "collect_ratings", "back"),
        ("feedback_complete", "start", "1"),
        ("feedback_complete", "end", "2")
    ]
    
    # Add transitions to the graph
    for src, dst, label in transitions:
        dot.edge(src, dst, label=label)
    
    # Render the graph
    dot.render('bbq_nation_state_machine', format='png', cleanup=True)
    print("State diagram generated: bbq_nation_state_machine.png")

if __name__ == "__main__":
    generate_state_diagram()
