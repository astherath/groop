# Data Visualizer
Web-based tool that can process, parse, and query a chat log file from a WhatsApp groupchat.

[Now in open beta.](http://felipearce.pw)

## Project Structure

- ### Frontend
 Clientside service was built with Reason using the BuckleScript JS compiler.
- ### File processing
Raw .txt formatter written in shell script, parser written in Go.
- ### Backend Services
Website served using Ubuntu + Nginx on a remote server. Serverside processes were written entirely in Python3. API endpoints written using Flask. Data visualizations and plots use Matplotlib and Pandas DataFrames, line of best fit uses Numpy.
- ### Database
All data stored in a local MongoDB instance, using the Pymongo driver for queries and insertions. User passwords were hashed + salted using bcrypt.

![Structure of service](architecture.png)

## Design Challenges
Whenever working with unprocessed, raw, real-life data, there were a few challenges to overcome. Such as:
- Contact names with emojis in them
- System messages (adding or removing participants, omitted media, chat title changes, etc.)
- Multi-line messages
- Inconsistent date formatting

All of the problems were with the data itself, so almost all of the time was spent writing processes to help sanitize the data. The most important solutions involved using regex to sanitize the contact names of emojis, and using variable width date parsers in Go.

## Future Features
(Listed in order of expected implementation date)
1. Plot messages over time for a single participant
2. Multiple group chat files per user
3. Timeline of addition/removal of participants from chat

## Feedback
If any unexpected or strange behavior occurs please open an issue request and it'll get sorted out quickly.
