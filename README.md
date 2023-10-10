# Steam Bulk Sell
An easy Steam market bulk sell script written in Python 3.

## Short Usage Instructions
It uses the geckodriver to interact with the Steam Market.
The newest version of the the geckodriver can be found [here](https://github.com/mozilla/geckodriver/releases).
Just download the driver and place it in the root directory of the repository.

## Long Usage Instructions
0. Prerequisits:
* git installed
  * For Windows users: [git-scm](https://git-scm.com/download/win)
  * For Linux users: please consult the package manager of you distro
* Python 3.11 installed
  * For Windows users: [python.org](https://www.python.org/downloads/)
  * For Linux users: please consult the package manager of you distro
* Pipenv installed
  * Install Pipenv following [this](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) instructions

1. Clone this repository:
* open a bash (or git bash for Windows users) 
* navigate to the folder where you want to install SteamBulkSell
* Paste and execute: `git clone https://github.com/Nerlant/SteamBulkSell.git`

2. Download geckodriver
* Download the geckodriver from [here](https://github.com/mozilla/geckodriver/releases)
* move the executable into the cloned repository

3. Install dependencies
* open a bash (or git bash for Windows users) 
* navigate to the folder where you want to install SteamBulkSell (cloned the repository)
* execute `pipenv install --ignore-pipfile`

4. Run script
* type `pipenv shell` to create a shell inside the venv
* type `python steam_market_bulk_sell.py` to start the script

5. Use the script
* Enter your steam username and password when prompted
* Wait for Firefox (geckodriver) to open and log you in
* Authenticate login when needed
* Wait until your inventory loads
* Select the type of item you want to sell (e.g. a CS:GO case)
* Enter the amount of items you want to sell
* Enter the amount of money you want to receive from each sold item
* Let the script do its job
* You may need to authenticate the sales in the Steam-App or by E-Mail
