with open("firestore.rules", "r") as f:
    content = f.read()

bad = """    match /users/{userId} {
      allow read, write: if isAuthenticated() && (request.auth.uid == userId || isAdmin());
      
      // Personal services subcollections
      match /favorites/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
      match /myCrops/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
      
      match /cart/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }"""

good = """    match /users/{userId} {
      allow read, write: if isAuthenticated() && (request.auth.uid == userId || isAdmin());
      
      // Personal services subcollections
      match /favorites/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
      match /myCrops/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
      
      match /cart/{documentId} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }"""

# Already looks correct, but let's just make sure
