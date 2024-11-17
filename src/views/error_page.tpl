<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frandrew Search - Error</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>

<body>
  % include('header.tpl')

  <div class="main-container">
    <div class="logo">FA</div>

    <h1>Error: {{ error_message }}</h1>
    <p>{{ error_description }}</p>

    <div class="error-details">
      <h2>What You Can Do:</h2>
      <ul>
        <li>Return to the <a href="/">home page</a>.</li>
        <li>If this issue persists, please contact support.</li>
      </ul>
    </div>

    <!-- Redirect Button -->
    <a href="/" class="back-button">Go Back to Home</a>
  </div>
</body>

</html>

