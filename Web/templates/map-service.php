// List points from database  
 
if ($_GET['action'] == 'listpoints') {
    $query = "SELECT * FROM tablename" ;  
    $result = map_query($query);  
    $points = array();
    while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {      
    array_push($points, array('name' => $row['name'],
    'lat' => $row['lat'], 'lng' => $row['lng'])); } 
    echo json_encode(array("locations" => $points));
    exit; 
}
// Save a point from our form 
 
if ($_POST['action'] == 'savepoint')
 {      $name = $_POST['name'];
    if(preg_match('/[^\w\s]/i', $name))
 {      fail('Invalid name provided.');
    }     
    if(empty($name))
     {    
     fail('Please enter a name.');      } 
 
// Query
$query = "INSERT INTO tablename SET name='$_POST[name]',
          address='$_POST[address]',  lat='$_POST[lat]',
          lng='$_POST[lng]' ";
$result = map_query($query);  
if ($result) {
    success(array('lat' => $_POST['lat'], 'lng' => $_POST['lng'],
    'address' => $_POST['address'], 'name' => $name));  
    }
    else {
    fail('Failed to add point.');   } 
    exit; 
    }
function map_query($query) {  
 
// Connect
mysql_connect('localhost', 'user' , 'password') OR
die(fail('Could not connect to database.'));  
mysql_select_db('database');
return mysql_query($query); }
 
function fail($message)
{die(json_encode(array('status' => 'fail', 'message' => $message)));}
 
function success($data)
{die(json_encode(array('status' => 'success', 'data' => $data)));}


CREATE TABLE 'tablename' (
  'id' int(11) unsigned NOT NULL auto_increment,
  'name' varchar(100) default NULL,
  'address' varchar(100) default NULL,
  'lat' float(15,11) default NULL,
  'lng' float(15,11) default NULL,
  PRIMARY KEY ('id')
)