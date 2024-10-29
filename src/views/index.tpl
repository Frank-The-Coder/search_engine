<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frandrew Search</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>

<body>
  % include('header.tpl')

  <div class="main-container">
    <div class="logo">FA</div>

    <form action="/search" method="post" class="search-container">
      <input type="text" name="keywords" class="search-bar" placeholder="Search..." required>
      <button type="submit" class="search-button">Search</button>
    </form>

    % if signedin:
    <h2>Most Recent Searches</h2>
    <table id="history">
      <thead>
        <tr>
          <th>Search Word</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        % for word, timestamp in recent_searches:
        <tr>
          <td>{{ word }}</td>
          <td>{{ timestamp }}</td>
        </tr>
        % end
      </tbody>
    </table>
    % end
  </div>
</body>

</html>