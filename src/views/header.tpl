<div class="user-info">
    % if signedin:
    <img src="{{ user_picture }}" alt="Profile Picture" class="profile-pic">
    <span>{{ user_name }} ({{ user_email }})</span>
    <a href="#" class="signout-button" id="logout-btn">Sign Out</a>
    % else:
    <a href="/login" class="login-button">Sign in with Google</a>
    % end
</div>

<script>
    document.getElementById('logout-btn')?.addEventListener('click', function (event) {
        event.preventDefault();

        fetch('/signout', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Logout failed. Please try again.');
                }
            })
            .catch(error => console.error('Error:', error));
    });
</script>