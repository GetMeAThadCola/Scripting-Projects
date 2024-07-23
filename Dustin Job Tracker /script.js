document.addEventListener('DOMContentLoaded', () => {
    const jobStatusElement = document.getElementById('job-status');
    const jobDurationElement = document.getElementById('job-duration');
    const loginForm = document.getElementById('login-form');
    const adminPanel = document.getElementById('admin-panel');
    const updateForm = document.getElementById('update-form');
    const jobStatusSelect = document.getElementById('job-status-select');
    const jobDurationInput = document.getElementById('job-duration-input');

    // Load stored data
    let jobStatus = localStorage.getItem('jobStatus') || 'No';
    let jobDuration = parseInt(localStorage.getItem('jobDuration')) || 0;
    let lastUpdated = new Date(localStorage.getItem('lastUpdated')) || new Date();

    // Update duration based on last update
    const currentDate = new Date();
    const daysDifference = Math.floor((currentDate - lastUpdated) / (1000 * 60 * 60 * 24));
    jobDuration += daysDifference;

    // Update UI
    function updateUI() {
        jobStatusElement.textContent = jobStatus;
        jobDurationElement.textContent = jobDuration;

        if (jobStatus === 'Yes') {
            jobStatusElement.classList.add('yes');
            jobStatusElement.classList.remove('no');
            jobDurationElement.classList.add('yes');
            jobDurationElement.classList.remove('no');
        } else {
            jobStatusElement.classList.add('no');
            jobStatusElement.classList.remove('yes');
            jobDurationElement.classList.add('no');
            jobDurationElement.classList.remove('yes');
        }
    }

    updateUI();

    // Save data
    function saveData() {
        localStorage.setItem('jobStatus', jobStatus);
        localStorage.setItem('jobDuration', jobDuration);
        localStorage.setItem('lastUpdated', new Date());
    }

    // Handle login
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const username = loginForm.username.value;
        const password = loginForm.password.value;

        // Simplified login check with complex password
        if (username === 'admin' && password === 'Roxas2020') {
            adminPanel.style.display = 'block';
            loginForm.style.display = 'none';
        } else {
            alert('Invalid login credentials!');
        }
    });

    // Handle update
    updateForm.addEventListener('submit', (event) => {
        event.preventDefault();
        jobStatus = jobStatusSelect.value;
        jobDuration = parseInt(jobDurationInput.value);

        updateUI();
        saveData();
    });
});
