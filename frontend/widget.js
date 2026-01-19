(function() {
  // Create the chat bubble button
  const button = document.createElement('div');
  button.style.position = 'fixed';
  button.style.bottom = '20px';
  button.style.right = '20px';
  button.style.width = '60px';
  button.style.height = '60px';
  button.style.backgroundColor = '#000';
  button.style.borderRadius = '50%';
  button.style.cursor = 'pointer';
  button.innerHTML = '💬'; // Or an SVG icon
  button.style.display = 'flex';
  button.style.alignItems = 'center';
  button.style.justifyContent = 'center';
  button.style.fontSize = '30px';
  button.style.zIndex = '9999';
  
  // Create the Iframe (Your Next.js App)
  const iframe = document.createElement('iframe');
  iframe.src = "https://your-deployed-frontend.com"; // WHERE YOU HOST NEXTJS
  iframe.style.position = 'fixed';
  iframe.style.bottom = '90px';
  iframe.style.right = '20px';
  iframe.style.width = '350px';
  iframe.style.height = '500px';
  iframe.style.border = 'none';
  iframe.style.borderRadius = '10px';
  iframe.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
  iframe.style.display = 'none'; // Hidden by default
  iframe.style.zIndex = '9999';

  document.body.appendChild(button);
  document.body.appendChild(iframe);

  // Toggle logic
  button.onclick = function() {
    if (iframe.style.display === 'none') {
      iframe.style.display = 'block';
    } else {
      iframe.style.display = 'none';
    }
  };
})();