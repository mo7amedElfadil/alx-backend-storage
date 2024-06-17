# 0x01-NoSQL: A MongoDb Guide


## CRUD

- Connect to database using `mongosh`

### Change or Create a database
```
use db_name
```

### Create a collection
- first method
    ```
    db.createCollection("posts")
    ```
- second method
    ```
    db.posts.insertOne(object)
    ```
given that object is a valid JSON 

### Inserting documents
- insert a single document

    ```
    db.posts.insertOne(object)
    ```
- insert many
    ```
    db.posts.insertMany(multipleCommaSeperatedObjects)
    ```

###  Finding data
    - finding multiple documents
    ```
    db.posts.find(optionalQueryObject) // if left empty, all docs will be returned
    ```
    - finding a single document (first match)
    ```
    db.posts.findOne(optionalQueryObject)
    ```
_Both find methods accept a second parameter called `projection`, which is an object that describes which fields to include in the results_

eg.
```
db.posts.find({}, {title: 1, date: 1})
```
**Note:**  the _id field is always included unless specifically excluded.

_We use a 1 to include a field and 0 to exclude a field._
```
db.posts.find({}, {_id: 0, title: 1, date: 1})
```
We can also exclude fields and the other fields will be included in the results
```
db.posts.find({}, {category: 0})
```
We will get an error if we try to specify both 0 and 1 in the same object (with the exlusion of _id from this rule)
```
db.posts.find({}, {title: 1, date: 0}) // yields an error
```

### Update Document
In both update methods the:
- 1st parameter is a query object to defind which document or documents should be updated
- 2nd parameter is an object defining the updated data

The `updateOne()` method will update the first document that is found matching the provided query.

```
db.posts.updateOne( { title: "Post Title 1" }, { $set: { likes: 2 } } )
```
    
**Note** the `$set` operator is used to update a specified field to a new value(patch update). If we dont use `$set`, the object at that id will be replaced with the new object. It will keep its id but all other fields will get dropped.

We can also use the `upsert` (_I guess update + insert had a child_) to insert if not fould
```
db.posts.updateOne( 
  { title: "Post Title 5" }, 
  {
    $set: 
      {
        title: "Post Title 5",
        body: "Body of post.",
        category: "Event",
        likes: 5,
        tags: ["news", "events"],
        date: Date()
      }
  }, 
  { upsert: true }
)
```
- The `updateMany()` method will update all documents that match the provided query.
```
db.posts.updateMany({}, { $inc: { likes: 1 } })
```
**Note** the `$inc` is the increment operator to update the field by 1.

### Delete Documents

The `deleteOne()` method will delete the first document that matches the query provided.
```
db.posts.deleteOne({ title: "Post Title 5" })
```

The `deleteMany()` method will delete all documents that match the query provided.
```
db.posts.deleteMany({ category: "Technology" })
```

## Query Operators

There are many query operators that can be used to compare and reference document fields.

### Comparison
The following operators can be used in queries to compare values:

`$eq:` Values are equal
`$ne:` Values are not equal
`$gt:` Value is greater than another value
`$gte:` Value is greater than or equal to another value
`$lt:` Value is less than another value
`$lte:` Value is less than or equal to another value
`$in:` Value is matched within an array

### Logical
The following operators can logically compare multiple queries.

`$and:` Returns documents where both queries match
`$or:` Returns documents where either query matches
`$nor:` Returns documents where both queries fail to match
`$not:` Returns documents where the query does not match

### Evaluation
The following operators assist in evaluating documents.

`$regex:` Allows the use of regular expressions when evaluating field values
`$text:` Performs a text search
`$where:` Uses a JavaScript expression to match documents


## Update Operators

There are many update operators that can be used during document updates.

### Fields
The following operators can be used to update fields:

`$currentDate:` Sets the field value to the current date
`$inc:` Increments the field value
`$rename:` Renames the field
`$set:` Sets the value of a field
`$unset:` Removes the field from the document

### Array
The following operators assist with updating arrays.

`$addToSet:` Adds distinct elements to an array
`$pop:` Removes the first or last element of an array
`$pull:` Removes all elements from an array that match the query
`$push:` Adds an element to an array

## Aggregation Pipelines
Aggregation operations allow you to group, sort, perform calculations, analyze data, and much more.

Aggregation pipelines can have one or more "stages". The order of these stages are important. Each stage acts upon the results of the previous stage.

eg. 
```
db.posts.aggregate([
  // Stage 1: Only find documents that have more than 1 like
  {
    $match: { likes: { $gt: 1 } }
  },
  // Stage 2: Group documents by category and sum each categories likes
  {
    $group: { _id: "$category", totalLikes: { $sum: "$likes" } }
  }
])
```

### Aggregation `$group`
This aggregation stage groups documents by the unique `_id` expression provided.

**Note** Don't confuse this `_id` expression with the `_id` ObjectId provided to each document.

```
db.listingsAndReviews.aggregate(
    [ { $group : { _id : "$property_type" } } ]
) // return the distinct values from the property_type field.
```

### Aggregation `$limit`
This aggregation stage limits the number of documents passed to the next stage.
```
db.movies.aggregate([ { $limit: 1 } ])
```

### Aggregation `$project`
This aggregation stage passes only the specified fields along to the next aggregation stage.

**Note** This is the same projection that is used with the `find()` method.

```
db.restaurants.aggregate([
  {
    $project: {
      "name": 1, // 1 for include, 0 exclude
      "cuisine": 1,
      "address": 1
    }
  },
  {
    $limit: 5
  }
])
```
**Note:** As mentioned previously you cannot use both 0 and 1 in the same object. The only exception is the `_id` field. You should either specify the fields you would like to include or the fields you would like to exclude.

### Aggregation `$sort`
This aggregation stage groups sorts all documents in the specified sort order.

**Note** Remember that the order of your stages matters. Each stage only acts upon the documents that previous stages provide.

```
db.listingsAndReviews.aggregate([ 
  { 
    $sort: { "accommodates": -1 } // 1 ascending, -1 descending order
  },
  {
    $project: {
      "name": 1,
      "accommodates": 1
    }
  },
  {
    $limit: 5
  }
])
```

### Aggregation `$match`
This aggregation stage behaves like a find. It will filter documents that match the query provided.

**Note:** Using `$match` early in the pipeline can improve performance since it limits the number of documents the next stages must process.

### Aggregation `$addFields`
This aggregation stage adds new fields to documents.
```
db.restaurants.aggregate([
  {
    $addFields: {
      avgGrade: { $avg: "$grades.score" }
    }
  },
  {
    $project: {
      "name": 1,
      "avgGrade": 1
    }
  },
  {
    $limit: 5
  }
])
```

### Aggregation $count
This aggregation stage counts the total amount of documents passed from the previous stage.
```
db.restaurants.aggregate([
  {
    $match: { "cuisine": "Chinese" }
  },
  {
    $count: "totalChinese"
  }
])
```
