from collections import defaultdict
import random      


# Gift exchange history stored in memory
# Key is sender, value is list of receiver(s) in past(maximum to 3) years
history = defaultdict(list)
    
def exchange_gifts(member_queryset):
    members = []
    for member in member_queryset:
        members.append(str(member.id))
    # Convert from list to set so that we can do set operations such as exclusion later
    receivers = set(members)
    
    # Current year gift exchange result
    # Key is sender (str representation), value is receiver
    result = {}
    for sender in members:
        eligible_receivers = receivers - {sender}
        eligible_receivers -= set(history[sender])
        if not eligible_receivers:
            # -1 means this year there is no eligible receiver for this sender
            receiver = '-1'
            result[sender] = receiver
        else:
            receiver = random.choice(list(eligible_receivers))
            result[sender] = receiver
            receivers.remove(receiver)

    # Update history
    for sender, receiver in result.items():
        history[sender].append(receiver)
        # Only keep 3 year's history for the constraint
        if len(history[sender]) > 3:
            history[sender].pop(0)

    return result
