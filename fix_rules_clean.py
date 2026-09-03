with open("firestore.rules", "r") as f:
    rules = f.read()

if "match /orders/{documentId}" not in rules:
    orders_rules = """
        match /orders/{documentId} {
          allow read: if isAuthenticated() && (resource.data.userId == request.auth.uid || isAdmin());
          allow create: if isAuthenticated() && request.resource.data.userId == request.auth.uid;
          allow update: if isAdmin();
        }
    """
    rules = rules.replace("match /{document=**} {", orders_rules + "\n    match /{document=**} {")

with open("firestore.rules", "w") as f:
    f.write(rules)
