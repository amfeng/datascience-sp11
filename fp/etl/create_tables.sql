CREATE DATABASE IF NOT EXISTS cs194;

use cs194;

CREATE TABLE IF NOT EXISTS badges (
    Date DATETIME,
    UserId INT,
    Id INT, 
    Name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS comments (
    CreationDate DATETIME,
    Text LONGTEXT,
    UserId INT,
    Score INT,
    PostId INT,
    Id INT,
    PRIMARY KEY(Id)
);

CREATE TABLE IF NOT EXISTS questions (
    Body LONGTEXT,
    ViewCount INT,
    LastActivityDate DATETIME,
    Title MEDIUMTEXT,
    LastEditorUserId INT,
    LastEditorDisplayName VARCHAR(255),
    LastEditDateTime DATETIME,
    CommentCount INT,
    AnswerCount INT,
    AcceptedAnswerId INT,
    Score INT,
    PostTypeId INT,
    OwnerUserId INT,
    Tags VARCHAR(255),
    CreationDate DATETIME,
    FavoriteCount INT,
    Id INT,
    PRIMARY KEY(Id)
);

CREATE TABLE IF NOT EXISTS answers (
    Body LONGTEXT,
    ViewCount INT,
    LastEditorDisplayName VARCHAR(255),
    LastEditorUserId INT,
    PostTypeId INT, 
    LastEditDate DATETIME,
    CommentCount INT,
    Score INT, 
    ParentId INT, 
    OwnerUserId INT,
    CreationDate DATETIME,
    Id INT,
    LastActivityDate DATETIME,
    PRIMARY KEY(Id)
);

CREATE TABLE IF NOT EXISTS users (
    DownVotes INT,
    DisplayName VARCHAR(255),
    Views INT,
    AboutMe MEDIUMTEXT,
    LastAccessDate DATETIME,
    WebsiteUrl MEDIUMTEXT,
    EmailHash VARCHAR(255),
    Reputation INT,
    Location MEDIUMTEXT,
    UpVotes INT,
    CreationDate DATETIME,
    Id INT
);

CREATE TABLE IF NOT EXISTS votes (
    VoteTypeId INT,
    PostId INT,
    Id INT,
    CreationDate DATETIME
);

CREATE TABLE IF NOT EXISTS tags (
    Tag VARCHAR(255),
    PostId INT,
    CreationDate DATETIME
);

CREATE TABLE IF NOT EXISTS toptags (
    Tag VARCHAR(255),
    Count INT
);

CREATE TABLE IF NOT EXISTS responsetimes (
    QuestionId INT,
    AnswerId INT,
    Tag VARCHAR(255),
    ResponseTime INT(15)
);

CREATE TABLE IF NOT EXISTS aggregate_responsetimes (
    QuestionId INT,
    Tag VARCHAR(255),
    AverageResponseTime INT(15),
    FastestResponseTime INT(15)
);

CREATE TABLE IF NOT EXISTS correct_responsetimes (
    QuestionId INT,
    Tag VARCHAR(255),
    CorrectResponseTime INT(15)
);

