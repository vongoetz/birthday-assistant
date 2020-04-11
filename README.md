# Birthday Assistant
A small system to automatically send customized email messages for important peoples' birthdays! Script pulls from spreadsheet that lists birthday information, and automatically deploys emails if the birthdate matches today. 

Script uses real SMTP mail servers so messages are not flagged as spam. Uses gmail.com by default, but may be configured to any mail server that allows. 

## Inspiration
Written for a special loved one to help him manage important birthdays. :)

## Usage
**(1) Configure birthday information in `CSV/birthdays.csv`**

- Sample file provided
- Birthdays must be in YYYY-MM-DD format
- `msg` field is optional for a custom message
- column `last_sent` should initially be left blank. 

Ideal circumstances: 
- update spreadsheet once a year
- don't change your email password

The latter is, of course, not realistic. :) A future release should include a **notification for when authentication fails.**

**(2) Add config.py file with single dictionary:**

```
sender_info = {
  'fromName': 'XXXXX',
  'fromFname': 'XXXXX',
  'fromLname': 'XXXXX',
  'fromEmail': 'XXXXX',
  'emailPass': 'XXXXX'
}
```

**(3) Configure email text in templates folder as HTML:**

```
<html>
  <head></head>
    <body><p>Build birthday message here!</p>
    <p>Use variables such as {tfname} or {ffname}.</p>
    <p> Insert {msg} here for custom message from spreadsheet</p>
    </body>
</html>
```

**(4) Set up on cron or other automated client-side service.**

# Outstanding TO DOs & Ideas:
- [ ] Deploy notification when authentication fails (e.g., password changes)
- [ ] Integrate with other mail servers
- [ ] Integrate with Google Calendar
- [ ] Chome plugin? Tons of applications