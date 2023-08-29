package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"server/db"
)

type Config struct {
	Port string
}

type Application struct {
	Config Config
	//TODO: add models
}

func (app *Application) Serve() error {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
		return err
	}

	port := os.Getenv("PORT")
	if port == "" {
		log.Fatal("$PORT must be set")
		return err
	}

	log.Printf("Listening on port %s", port)

	srv := &http.Server{
		Addr: fmt.Sprintf(":%s", port),
		//TODO: add router
	}

	return srv.ListenAndServe()
}

func main() {
	fmt.Println("Hello there!")

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", os.Getenv("DB_HOST"), os.Getenv("DB_PORT"), os.Getenv("DB_USER"), os.Getenv("DB_PASSWORD"), os.Getenv("DB_NAME"))

	dbConn, err := db.Connect(dsn)
	if err != nil {
		log.Fatal("Error connecting to database", err)
	}

	defer dbConn.DB.Close()

	app := Application{
		Config: Config{
			Port: os.Getenv("PORT"),
		},
	}

	err = app.Serve()
	if err != nil {
		log.Fatal(err)
	}
}
