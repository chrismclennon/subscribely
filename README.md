## Subscribely

Subscribely is a subscription management service. Subscribe or unsubscribe from popular services with a single click, and save money along the way.

## How

Subscribely is powered by [Modo Payments](http://www.modopayments.com). When a user subscribes to a service, Subscribely uses Modo to charge the customer's credit card and creates a new, virtual credit card. Subscribely then screen scrapes into the service to subscribe the user with the virtual credit card. When a user subscribes by gift card, Subscribely uses Modo to generate a gift card which is screen scraped into the service.

How does it save you money? Subscribely uses Modo to generate gift cards at a discount, and we pass those savings to you!

## Development Setup
`brew install python3`  
`brew install chromedriver`  
`pip3 install --editable .`  
`export FLASK_APP=subscribely`  
`export MODO_API_KEY=`  
`export MODO_API_SECRET_KEY=`  

## Running the App Locally
`flask initdb`  
`flask run`  
Runs on http://localhost:5000/ by default.

## Contributors
Cecile Nguyen (@cecileceng)  
Matt Groot (@wmgroot)  
Chris McLennon (@cmclen)
