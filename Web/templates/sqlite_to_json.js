function sqliteToJSON() {

	newJson = {
		$resources: []
	};

	offlinedb = openDatabase (shortName, version, displayName, maxSize);

	offlinedb.transaction(function(transaction) {

		transaction.executeSql('SELECT * FROM location;', [],
		
		function(transaction, result) {

			if (result !== null && result.rows !== null) {

				for (var k = 0; k < result.rows.length; k++) {

					var row = result.rows.item(k);

					if(k > 0) newJson += ',';
					newJson.$resources[k] = row;
				}

				jsonall = JSON.stringify(newJson);

				// jsonall = JSON.stringify(result.rows);
   
				alert(jsonall); //shows me a correct JSON as string

				jsonobjoff = $.parseJSON(jsonall);

				for (i = 0; i < jsonobjoff.$resources.length; i++) {

					$('#json').append("<li>" + jsonobjoff.$resources[i].Field0 + " " + jsonobjoff.$resources[i].Field1 + " " + jsonobjoff.$resources[i].Field2 + " " + jsonobjoff.$resources[i].Field3 + " " + jsonobjoff.$resources[i].Field4 + " " + jsonobjoff.$resources[i].Field5 + "</li>");
				}
			}

		},errorHandler);

	},errorHandler, nullHandler);

}