# TIME MANAGEMENT Network
## Technical task

Note: that's simply a `markdown` slightly refactored version of a [technical_task.pdf](technical_task.pdf)


### User Interface

The project is a kind of on-line service for time management and tracking of statistics about the time spent under the control
of your personal program

Each user will have the opportunity to register on their own, then use the provided login or mail + password to login. At his disposal, he has a personal timer that allows you to measure the necessary time interval for a certain task (for example, 20 minutes to read a book), while in the application itself, the session start time and end time will be tracked by the user submitting corresponding signals. This way the user session log will be stored when it starts a new session and ends with a "controlled time waste" session.

For the user, statistics will be available in which he can look at the total time spent, the average time of the session, his ”level” at the moment (which will be calculated according to a certain formula + our secret sauce), as well as the amount of time he spends consciously per day average.

There will be an opportunity to subscribe or unsubscribe from a our mailing system: it will track how interested is user in our articles, if he likes them and reads those which we send him in mails - we will track that and send him more of them, or maybe less but more often (more mails with less content, so he can keep up with new information).


### Database Structure

The database will consist of 4 tables:


* table `Users`
```
userid
username
useremail
userpassword
```

* table `Sessions_log`
```
sessionid
userid
type
timestamp
```

* table `User_experience`
```
- userid
- totaltimespent
- amountoffinishedsessions
```

* table `Mailing_list`
```
- userid
- emailsubscriptionagreement
- lastnotification
- notificationclickthroughrate

```

* table `Groups`:
```
- groupid
- type
- groupname
```
