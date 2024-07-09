const firebaseConfig = {
  apiKey: "AIzaSyBcTEVvxXmv5N8dJav4xNDRy5hXZRjVeM4",
  authDomain: "chatflow-59776.firebaseapp.com",
  databaseURL: "https://chatflow-59776-default-rtdb.firebaseio.com",
  projectId: "chatflow-59776",
  storageBucket: "chatflow-59776.appspot.com",
  messagingSenderId: "549003131640",
  appId: "1:549003131640:web:3f4a7b8cef4c0d8a2b990d",
  measurementId: "G-V2180PR5CR"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const storage = firebase.storage();

// Reference to the "profilesphoto" folder
const storageRef = storage.ref().child('profilesphoto');

// Get all photos in the "profilesphoto" folder
storageRef.listAll().then(result => {
    result.items.forEach(imageRef => {
        displayImage(imageRef);
    });
}).catch(error => {
    console.error('Error listing all photos:', error);
});

// Display image in the container
function displayImage(imageRef) {
    imageRef.getDownloadURL().then(url => {
        const img = document.createElement('img');
        img.src = url;
        document.getElementById('photo-container').appendChild(img);
    }).catch(error => {
        console.error('Error getting image URL:', error);
    });
}
