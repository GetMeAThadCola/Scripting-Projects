const nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: 'example@example.com', // Use the email you want to send from here
        pass: 'Your_App_Password', // Use an app password generated in your Gmail settings
    },
});

function sendResetLink(email) {
    // Generate a random reset token (for simulation purposes)
    const resetToken = Math.random().toString(36).substring(2, 10);

    let mailOptions = {
        from: 'example', // Replace with your email address for example
        to: email,
        subject: 'Password Reset Link',
        text: `Your password reset link: https://yourwebsite.com/reset?token=${resetToken}`, // Change to your website
    };

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log('Error:', error);
        } else {
            console.log('Password reset link sent to: ' + email);
        }
    });
}

// Usage example: Replace 'recipient@example.com' with the actual recipient's email
sendResetLink('recipient@example.com');