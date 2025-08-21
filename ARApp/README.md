#Steps
## local web server with HTTPS
1. XAMMP
2. or, Install Visual Code extension "Live Server", which is used to launch a development local server with a live reload feature for static & dynamic pages. Supports dynamic pages like PHP.

## create a self-signed SSL Certificate
1. Download and Install Openssl: https://slproweb.com/products/Win32OpenSSL.html. Add "C:\Program Files (x86)\GnuWin32\bin" to PATH. Add environment variable OPENSSL_CONF=C:\Program Files (x86)\GnuWin32\share\openssl.cnf
2. Generating a Private Key and Self-Signed Certificate: openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes -keyout localhost1.key -out localhost1.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"
3.  Install the Certificate into Chrome’s Trust Store: Windows: Double-click the .crt file to open the Certificate Import Wizard. Choose "Place all certificates in the following store" and select "Trusted Root Certification Authorities.". Restart Chrome.

## enable HTTPS on Live Sever
1. Create .vscode folder inside the project.
2. Inside that folder create settings.json file
3. Paste the following code:
{
    "liveServer.settings.root": "/",
    "liveServer.settings.https": {
    "enable": true, //set it true to enable the feature.
    "cert": "C:\\dev\\workspace\\certs\\localhost1.crt", //full path of the certificate
    "key": "C:\\dev\\workspace\\certs\\localhost1.key", //full path of the private key
    "passphrase": "12345678"
    }
}
4. Right click on any html file, and select "Open in Live Sever", or click "Go Live" at bottom right of task bar.
