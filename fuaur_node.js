const axios = require('axios');

// The URL you want to send the POST requests to
const url = 'https://alegerilibere.ro/petitie.php'; // Replace with the actual URL

// The body data for the POST requests
const postData = {
    accept_gdpr: 'on',
    nume: 'Random message', // You can modify this or use a dynamic message
    phone: '0720123455666',
    t: 'h5t07vsh2vjgc6b8fgm0g0cqbi',
    tara: 'Africa de Sud'
};

// Function to send a POST request
const sendPostRequest = async () => {
    try {
        const response = await axios.post(url, postData);
        console.log('Response Status:', response.status);
    } catch (error) {
        console.error('Error sending POST request:', error);
    }
};

// Send multiple POST requests
const sendMultipleRequests = async (numberOfRequests) => {
    for (let i = 0; i < numberOfRequests; i++) {
        console.log(`Sending request #${i + 1}`);
        await sendPostRequest();
    }
};

sendMultipleRequests(1000000);