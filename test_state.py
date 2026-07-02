from state import StateManager

# Create State Manager
state = StateManager()

print("Current State:")
print(state.state)

print("\nChecking if ID '123' exists...")
print(state.is_processed("123"))

print("\nMarking '123' as processed...")
state.mark_processed("123")

print("\nChecking again...")
print(state.is_processed("123"))

print("\nFinal State:")
print(state.state)