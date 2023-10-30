// Function to generate a random password reset token
function generateResetToken(length) {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const charsetLength = charset.length;

    let token = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charsetLength);
        token += charset[randomIndex];
    }

    return token;
}

// Example usage
const tokenLength = 12; // Define the length of the token
const resetToken = generateResetToken(tokenLength);
console.log('Generated Reset Token:', resetToken);
