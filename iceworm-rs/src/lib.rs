/*
TODO:
 - pumps
 - cancel (poll in rs), get progress (generalized op status? + generic 'progress'?)
 - parquet
 - destructure
  - embeds_one/embeds_many - -> table with fk
  - has_and_belongs_to_many -> table of 2 fks
*/
use csv::Error;

extern crate postgres;
extern crate postgres_openssl;

use postgres::{Client, NoTls};

use pyo3::buffer::PyBuffer;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

extern crate rusoto_core;
extern crate rusoto_s3;

use rusoto_core::{Region, ByteStream};
use rusoto_s3::{S3, S3Client, PutObjectRequest};

extern crate tokio;

use tokio::runtime::Runtime;


fn _hit_postgres() -> () {
    let mut client = Client::connect(
        "host=localhost port=23123 user=iceworm password=iceworm",
        NoTls,
    ).unwrap();

    client.batch_execute("
    DROP TABLE IF EXISTS person
    ").unwrap();

    client.batch_execute("
    CREATE TABLE person (
        id      SERIAL PRIMARY KEY,
        name    TEXT NOT NULL,
        data    BYTEA
    )
    ").unwrap();

    let name = "Ferris";
    let data = None::<&[u8]>;
    client.execute(
        "INSERT INTO person (name, data) VALUES ($1, $2)",
        &[&name, &data],
    ).unwrap();

    for row in client.query("SELECT id, name, data FROM person", &[]).unwrap() {
        let id: i32 = row.get(0);
        let name: &str = row.get(1);
        let data: Option<&[u8]> = row.get(2);

        println!("found person: {} {} {:?}", id, name, data);
    };
}

#[pyfunction]
fn hit_postgres() -> PyResult<()> {
    _hit_postgres();

    Ok(())
}

#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


#[test]
fn test_hit_postgres() {
    _hit_postgres();
}

// #[test]
// fn test_s3() {
//     let mut rt = Runtime::new().unwrap();
//
//     let s3_client = S3Client::new(Region::UsEast1);
//     let fut = s3_client.put_object(PutObjectRequest {
//         bucket: String::from("bucket"),
//         key: "@types.json".to_string(),
//         body: Some(ByteStream::from(b"hi".to_vec())),
//         acl: Some("public-read".to_string()),
//         ..Default::default()
//     });
//
//     let x = rt.block_on(fut);
//     x.expect("could not upload");
// }

#[test]
fn test_csv() {
    let csv = "year,make,model,description
        1948,Porsche,356,Luxury sports car
        1967,Ford,Mustang fastback 1967,American car";

    let mut reader = csv::Reader::from_reader(csv.as_bytes());
    for record in reader.records() {
        let record = record.unwrap();
        println!(
            "In {}, {} built the {} model. It is a {}.",
            &record[0],
            &record[1],
            &record[2],
            &record[3]
        );
    }

    // let mut wtr = csv::Writer::from_path("foo.csv").unwrap();
    // wtr.write_record(&["a", "b", "c"]).unwrap();
    // wtr.write_record(&["x", "y", "z"]).unwrap();
    // wtr.flush().unwrap();
}

#[test]
fn test_mongo() {
    let client = mongodb::sync::Client::with_uri_str("mongodb://localhost:27017").unwrap();
    let database = client.database("mydb");
    let collection = database.collection("books");

    let docs = vec![
        bson::doc! { "title": "1984", "author": "George Orwell" },
        bson::doc! { "title": "Animal Farm", "author": "George Orwell" },
        bson::doc! { "title": "The Great Gatsby", "author": "F. Scott Fitzgerald" },
    ];

    collection.insert_many(docs, None).unwrap();

    let cursor = collection.find(bson::doc! { "author": "George Orwell" }, None).unwrap();
    for result in cursor {
        match result {
            Ok(document) => {
                if let Some(title) = document.get("title").and_then(bson::Bson::as_str) {
                    println!("title: {}", title);
                } else {
                    println!("no title found");
                }
            }
            Err(e) => ()
        }
    };
}