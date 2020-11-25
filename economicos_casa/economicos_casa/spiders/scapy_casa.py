import scrapy

#resumen=response.xpath('//div[@class="col2 span6"]/a/h3/text()').getall()
#precio=response.xpath('//li[@class="ecn_precio"]/text()').getall()
#btn siguiente y ultimo ('response.xpath("//div[@class='cont_right_ecn_pag']/a/@href").getall())
#npagina=response.xpath ('//span[@class="pag_resul_bus_0 pag_resul_bus"]/strong/text()').getall()

class scrapy_casa(scrapy.Spider):
    name='casa'
    start_urls=['http://www.economicos.cl/todo_chile/casa?operacion=Venta'
    ]
    custom_settings={
        'FEED_URI':'casas.json',
        'FEED_FORMAT':'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    
    def formatear_precio(self,precios):
        precios_new=[]
        for precio in precios:
            precio=precio.replace("\n","")
            precio=precio.replace("\t","")
            precio=precio.replace(" ","")
            if precio!="":
                precios_new.append(precio)
            else:
                pass
        return precios_new
    
    def format_descripcion_precio(self,resumen,precios):
        precios_new=self.formatear_precio(precios)
        reg=[]
        for x in range(len(resumen)):
            reg.append("Descripcion: "+resumen[x]+", Precio: "+precios_new[x])
        return(reg)

    def parse(self,response):
        resumenes=response.xpath('//div[@class="col2 span6"]/a/h3/text()').getall()
        precios=response.xpath('//li[@class="ecn_precio"]/text()').getall() 
        btn_next_prev=response.xpath('//div[@class="cont_right_ecn_pag"]/a/@href').getall()
        reg=self.format_descripcion_precio(resumenes,precios)
        if len(btn_next_prev)==2:
            yield response.follow(btn_next_prev[0],callback=self.parse_only,cb_kwargs={'reg': reg})
        else:                  
            yield response.follow(btn_next_prev[1],callback=self.parse_only,cb_kwargs={'reg': reg})
        
    def parse_only(self,response,**kwargs):
        if kwargs:
            regis=kwargs['reg']
        npagina=response.xpath('//span[@class="pag_resul_bus_0 pag_resul_bus"]/strong/text()').getall()
        resumenes=response.xpath('//div[@class="col2 span6"]/a/h3/text()').getall()
        precios=response.xpath('//li[@class="ecn_precio"]/text()').getall() 
        btn_next_prev=response.xpath('//div[@class="cont_right_ecn_pag"]/a/@href').getall()
        reg=self.format_descripcion_precio(resumenes,precios)
        if npagina[0]=="5":
            yield {
                'registros':regis
            }
        else:
            yield response.follow(btn_next_prev[1],callback=self.parse_only,cb_kwargs={'reg': reg})
        



 
        
