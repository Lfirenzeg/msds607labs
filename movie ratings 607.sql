-- When runnig this code we have to drop the Ratings table first (since it has foreign key constraints on Movies and People)
-- Make sure to download the 3 csv files people, movies and ratings, and save them on a path that SQL can load them from to avoid error 1290
-- URL to download files: https://github.com/Lfirenzeg/msds607labs

DROP TABLE IF EXISTS Ratings;
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS People;

-- Create Movies table
CREATE TABLE Movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    release_year INT,
    genre VARCHAR(50)
);

-- Create People table
CREATE TABLE People (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10)
);

-- Create Ratings table (with foreign keys)
CREATE TABLE Ratings (
    movie_id INT,
    person_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    PRIMARY KEY (movie_id, person_id),
    FOREIGN KEY (person_id) REFERENCES People(person_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

-- Load People data
-- To ensure the code is reproducible, replace the directory after INFILE with whatever 
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/people.csv'
INTO TABLE People
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(name, age, gender);

-- Load Movies data
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movies.csv'
INTO TABLE Movies
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(title, release_year, genre);

-- Load Ratings data, ensuring person_id and movie_id match those in People and Movies
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings.csv'
INTO TABLE Ratings
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(movie_id, person_id, rating);

SELECT People.name, Movies.title, Ratings.rating
FROM Ratings
JOIN People ON Ratings.person_id = People.person_id
JOIN Movies ON Ratings.movie_id = Movies.movie_id
WHERE Movies.title = 'barbie';

