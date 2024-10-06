<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Frandrew Search</title>
  <link rel="stylesheet" type="text/css" href="/static/css/style.css">
  <style>
  </style>
</head>

<body>
  <div class="logo">
    FA
  </div>
  <form action="/search" method="post" class="search-container">
    <input type="text" name="keywords" class="search-bar" placeholder="Search..." autofocus>
    <button type="submit" class="search-button">Search</button>
  </form>
  <h2> Top 20 words search history </h2>
  % if len(top_20_list) != 0:
  <table id="history">
      <thead>
          <tr>
              <th>Word</th>
              <th class="text_left_align">Count</th>
          </tr>
      </thead>
      <tbody>
          % for (count, word) in top_20_list:
          <tr>
              <td>{{ word }}</td>
              <td class="text_left_align">{{ count }}</td>
          </tr>
          % end
      </tbody>
  </table>
  % else:
  The current search history is empty, start searching!
  % end
</body>

</html>
