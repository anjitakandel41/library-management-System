// ================= Login/Register Toggle =================
const signUpButton = document.getElementById('signUpButton');
const signInButton = document.getElementById('signInButton');
const signInForm = document.getElementById('signIn');
const signUpForm = document.getElementById('signup');

signUpButton.addEventListener('click', function() {
    signInForm.style.display = "none";
    signUpForm.style.display = "block";
});

signInButton.addEventListener('click', function() {
    signInForm.style.display = "block";
    signUpForm.style.display = "none";
});

// ================= Dashboard Tabs Toggle =================
// Only runs on dashboard page
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab-button');
    const sections = document.querySelectorAll('.tab-section');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const target = this.dataset.target;

            // Hide all sections
            sections.forEach(section => section.style.display = "none");
            
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active-tab'));

            // Show the selected section
            document.getElementById(target).style.display = "block";
            this.classList.add('active-tab');
        });
    });
});

// ================= Confirmation for Return/Issue =================
function confirmAction(message) {
    return confirm(message);
}
