import psycopg2
import web
import json


web.config.debug = False        ## Used for Debugging

urls = (                        ##Consists of urls and classes coresponding to that urls
    '/', 'ApiOne',
    '/(js|css|images)/(.*)', 'static',
)


class static:

    """Static class is used to make path for various Directories embedded in static directory.
    It corresponds to static url and is mostly used for linking Chart.js to template."""

    def GET(self, media, file):
        try:
            f = open(media + '/' + file, 'r')
            return f.read()
        except:
            # you can send an 404 error here if you want
            return 'Cant find the file' + str(file)


class ApiOne():

    """ApiOne is implementation of Api#1.It provides both ingestion and output respectively.
   It uses various libraries and corresponds to '/' url.It also contains GET and POST methods for
   template rendering."""  

    conn = psycopg2.connect(database="Assignment", user="welcome",
                            password="Test123#", host="localhost", port="5432")

    def Create_Table(self):

        """Method is used to create Table and also provides a glimpse of basic schema
        to the developer."""

        with open('data.csv', 'r') as fileop:
            for each_line in fileop:
                columns = each_line.split(',')
                columns[-1] = columns[-1].strip()
                print(columns)
                break

        query = "CREATE TABLE data ("
        query = query + "id integer,"
        query = query + columns[1] + " integer,"  # 'awb'
        query = query + columns[2] + " integer,"  # 'breadth'
        query = query + columns[3] + " varchar,"  # 'buyer_city'
        query = query + columns[4] + " integer,"  # 'buyer_pin'
        query = query + columns[5] + " timestamp,"  # 'cancelled_date'
        query = query + columns[6] + " varchar,"  # 'current_status'
        query = query + columns[7] + " timestamp,"  # 'delivered_date'
        query = query + columns[8] + " integer,"  # 'delivery_attempt_count'
        query = query + columns[9] + " timestamp,"  # 'dispatch_date'
        query = query + columns[10] + " bool,"  # 'heavy'
        query = query + columns[11] + " integer,"  # 'height'
        query = query + columns[12] + " timestamp,"  # 'last_mile_arrival_date'
        query = query + columns[13] + " timestamp,"  # 'last_modified'
        query = query + columns[14] + " integer,"  # 'length'
        query = query + columns[15] + " timestamp,"  # 'order_created_date'
        query = query + columns[16] + " varchar PRIMARY KEY,"  # 'order_id'
        query = query + columns[17] + " integer,"  # 'price'
        query = query + columns[18] + " varchar,"  # 'product_category'
        query = query + columns[19] + " varchar,"  # 'product_id'
        query = query + columns[20] + " varchar,"  # 'product_name'
        query = query + columns[21] + " integer,"  # 'product_price'
        query = query + columns[22] + " integer,"  # 'product_qty'
        query = query + columns[23] + " timestamp,"  # 'promised_date'
        query = query + columns[24] + " varchar,"  # 'return_cause'
        # 'reverse_logistics_booked_date'
        query = query + columns[25] + " timestamp,"
        query = query + columns[26] + " timestamp,"  # 'reverse_logistics_date'
        # 'reverse_logistics_delivered_date'
        query = query + columns[27] + " timestamp,"
        query = query + columns[28] + " timestamp,"  # 'rto_date'
        query = query + columns[29] + " timestamp,"  # 'rto_delivered_date'
        query = query + columns[30] + " varchar,"  # 'seller_city'
        query = query + columns[31] + " integer,"  # 'seller_pin'
        # 'shipper_confirmation_date'
        query = query + columns[32] + " timestamp,"
        query = query + columns[33] + " varchar,"  # 'shipper_name'
        query = query + columns[34] + " integer,"  # 'shipping_cost'
        query = query + columns[35] + " integer );"  # 'weight'
        curs = self.conn.cursor()
        try:
            curs.execute(query)
        except:
            return 'Table creation failed.Table already exists or wrong datatype used.'
        print("Table created.")
        curs.close()
        self.conn.commit()
        self.conn.close()

    def ignore_if_no_id(self, line):

        #Used to ignore first line of data.csv

        try:
            if line.split(',')[0] == '':
                return True
            else:
                return False
        except:
            print("First line is not same.Wrong type of csv file.")
            return False

    def ingest_row_by_row(self):

        #Used to ingest data row by row.

        with open('data.csv', 'r') as fileobj:
            for eachline in fileobj:
                if not self.ignore_if_no_id(eachline):
                    row = eachline.split(',')
                    row[-1] = row[-1].strip()
                    query = "INSERT INTO data VALUES ("
                    for element in row:
                        if element == '':
                            query = query + 'NULL,'
                        else:
                            if "'" in element:
                                query = query + "'" + \
                                    str(element.replace("'", "''")) + "',"
                            else:
                                query = query + "'" + str(element) + "',"
                    query = query[:-1]
                    query = query + ");"
                    print(query)
                    curs = self.conn.cursor()
                    try:
                        curs.execute(query)
                    except:
                        return 'Insertion failed.Check query again.'
                    self.conn.commit()
                    curs.close()

    def ingest_multiple_row(self,params):

        #Used to ingest data through multiple Number of Row. Number being provided in parameter.

        i=0
        with open('data.csv', 'r') as fileob:
            query = "INSERT INTO data VALUES "
            for eachline in fileob:
                if not self.ignore_if_no_id(eachline) and i<=params:
                    i=i+1
                    row = eachline.split(',')
                    row[-1] = row[-1].strip()
                    query = query+"("
                    print(eachline)
                    for each in row:
                        if each == '':
                            query = query + 'NULL,'
                        else:
                            if "'" in each:
                                query = query + "'" + \
                                    str(each.replace("'", "''")) + "',"
                            else:
                                query = query + "'" + str(each) + "',"

                    query = query[:-1]
                    query = query + "),"
            query = query[:-1]
            query = query + ";"
            print(query)
            curs = self.conn.cursor()
            try:
                curs.execute(query)
            except:
                return 'Insertion failed.Check query again.'
            self.conn.commit()
            curs.close()	        				


##-------------------------------------------------Output--------------------------------------##

    def output(self, order_id_list=None, parameter=None):

        """ Method is used to Output shipper name for sql table with the help of provided parameters.
        parameters are list or list of lists."""

        query = "SELECT shipper_name FROM data WHERE "
        if order_id_list:
            query = query + "order_id IN ("
            for ids in order_id_list:
            	query = query + "'" + str(ids) + "',"
            query = query[:-1]
            query = query + ");"
            print(query)
        else:
            query = query + "seller_city IN ("
            try:
            	trial = parameter[0][0]
            	for cities in parameter[0]:
            		query = query + "'" + str(cities) + "',"
                query = query[:-1]
                query = query + ") AND "
            except:
                return ["Not Inputted Sellar location.Please Input Sellar location Or search by OrderId."]

            query = query + "buyer_city IN ("
            try:
                trial = parameter[1][0]
                for cities in parameter[1]:
                	query = query + "'" + str(cities) + "',"
                query = query[:-1]
                query = query + ") AND "
            except:
                return ["Not Inputted Buyer location.Please Input Buyer location Or search by OrderId."]

            if parameter[2]:
                query = query + "product_category IN ("
                for cities in parameter[2]:
                	query = query + "'" + str(cities) + "',"
                query = query[:-1]
                query = query + ") AND "

            query = query[:-5]
            query = query + ";"
        curs = self.conn.cursor()
        print(query)
        try:
        	curs.execute(query)
        except:
        	return ["Query went wrong. Please check if server is running or not.Then check entered query."]
        shipper_name = []
        for cur in curs:
            shipper_name.append(str(cur[0]))
        return shipper_name

    def count(self, param_date):

        """Method is used to output single count at provided date."""

        query = "SELECT count(shipper_name) FROM data WHERE date(order_created_date) = "
        query = query + "'" + param_date + "';"
        curs = self.conn.cursor()
        curs.execute(query)
        return str(curs.fetchone()[0])

    def countall(self):

        """Uses count method to extrat data of all dates.Result is return in dictionary format."""

    	dates = []
        counts = []
        query = "SELECT DISTINCT(date(order_created_date)) FROM data ORDER BY date(order_created_date) ASC ;"
        curs = self.conn.cursor()
        curs.execute(query)
        for each in curs:
            dates.append(str(each[0]))
            counts.append(self.count(str(each[0])))
        jsonob = {"dates": dates, "counts": counts}
        return jsonob

    def make_empty(self,alist):

        #Used to make a list empty

    	if alist == ['']:
    		alist =[]
    		return alist
    	return alist 

    def GET(self):

        """ GET function of ApiOne that renders the basic template to be loaded.Currently GET is used to dump dictionary returned
        data from countall into json and provide it to template to be rendered."""

        jsonob = self.countall() 
        output = ''
        render = web.template.render('')
        return render.WebApp(json.dumps(jsonob), output)

    def POST(self):

        """ POST of ApiOne that request the input data , passes this data to output method.Then returned data from output 
        method is then provided to the rendered template in string format.It also renders the same json data that GET uses."""
    	jsonob = self.countall()
        shipper = []
        data = web.input()
        orderid = str(data.order_id).split(',')
        sellarlocation = str(data.sellar_city).split(',')
        buyerlocation = str(data.buyer_city).split(',')
        productcategory = str(data.product_category).split(',')

        orderid = self.make_empty(orderid)
        sellarlocation = self.make_empty(sellarlocation)
        buyerlocation = self.make_empty(buyerlocation)
        productcategory = self.make_empty(productcategory)

        shipper = self.output(orderid,[sellarlocation, buyerlocation, productcategory])
        if shipper==[]:
        	shipper=["Not Found any shipper names with provided parameters."]
        render = web.template.render('')
        shipper = str(shipper).replace('[','').replace(']','').replace("'",'')
        shipper = shipper + " is output shipper name(s)."
        return render.WebApp(json.dumps(jsonob),shipper)


### Main function is loaded and calls the respective urls to runserver and Apis.       

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
