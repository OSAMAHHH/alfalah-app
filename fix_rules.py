with open("firestore.rules", "r") as f:
    rules = f.read()

# Add cart to users subcollections
cart_rules = """
      match /cart/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
"""
rules = rules.replace("match /conversations/{documentId} {", cart_rules + "      match /conversations/{documentId} {")

# Add orders collection
orders_rules = """
    match /orders/{documentId} {
      allow read: if isAuthenticated() && (resource.data.userId == request.auth.uid || isAdmin());
      allow create: if isAuthenticated() && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin();
    }
"""
rules = rules.replace("match /{document=**} {", orders_rules + "    match /{document=**} {")

with open("firestore.rules", "w") as f:
    f.write(rules)
