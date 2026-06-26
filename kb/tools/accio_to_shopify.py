#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Accio Work 选定产品 → Shopify 标准商品导入 CSV(默认 draft,待人审后发布)。
用法:  python accio_to_shopify.py 选品.json -o shopify_products.csv
输入:  JSON 数组或 CSV;字段灵活(见 FIELD_MAP)。最少需要 product_name/title。
注意:  本工具只做"数据转换",不下单/不付款;价格/成本/认证请人工复核后再发布。"""
import json,csv,sys,re,argparse,os
FIELD={"title":["title","product_name","name","产品名","品名"],
"vendor":["vendor","supplier","供应商","厂商"],
"price":["price","suggested_price","retail_price","售价","建议零售价"],
"cost":["cost","unit_cost","成本","采购价"],
"moq":["moq","min_order","起订量"],
"category":["category","type","品类","类目"],
"market":["market","target_market","目标市场"],
"image":["image","image_url","img","图片"],
"certs":["certifications","certs","认证"],
"sku":["sku","SKU"],
"desc":["description","notes","desc","卖点","描述"]}
def get(row,key):
    for k in FIELD[key]:
        for rk in row:
            if rk.lower()==k.lower() and str(row[rk]).strip(): return str(row[rk]).strip()
    return ""
def handle(t): 
    h=re.sub(r"[^a-z0-9一-鿿]+","-",t.lower()).strip("-"); return h or "product"
def load(p):
    if p.endswith(".json"): return json.load(open(p,encoding="utf-8"))
    return list(csv.DictReader(open(p,encoding="utf-8")))
COLS=["Handle","Title","Body (HTML)","Vendor","Type","Tags","Published",
"Option1 Name","Option1 Value","Variant SKU","Variant Inventory Tracker","Variant Inventory Qty",
"Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Requires Shipping",
"Variant Taxable","Image Src","Image Alt Text","Status",
"Metafield: custom.supplier [single_line_text_field]","Metafield: custom.cost [number_decimal]",
"Metafield: custom.moq [number_integer]","Metafield: custom.certifications [single_line_text_field]",
"Metafield: custom.target_market [single_line_text_field]"]
def convert(rows):
    out=[]
    for i,r in enumerate(rows,1):
        t=get(r,"title")
        if not t: continue
        sku=get(r,"sku") or f"ACCIO-{i:04d}"
        tags=[x for x in [get(r,"category"),get(r,"market"),"accio-sourced"] if x]
        out.append({"Handle":handle(t),"Title":t,"Body (HTML)":get(r,"desc"),
        "Vendor":get(r,"vendor"),"Type":get(r,"category"),"Tags":", ".join(tags),"Published":"FALSE",
        "Option1 Name":"Title","Option1 Value":"Default Title","Variant SKU":sku,
        "Variant Inventory Tracker":"shopify","Variant Inventory Qty":"0",
        "Variant Inventory Policy":"deny","Variant Fulfillment Service":"manual",
        "Variant Price":get(r,"price"),"Variant Requires Shipping":"TRUE","Variant Taxable":"TRUE",
        "Image Src":get(r,"image"),"Image Alt Text":t,"Status":"draft",
        "Metafield: custom.supplier [single_line_text_field]":get(r,"vendor"),
        "Metafield: custom.cost [number_decimal]":get(r,"cost"),
        "Metafield: custom.moq [number_integer]":get(r,"moq"),
        "Metafield: custom.certifications [single_line_text_field]":get(r,"certs"),
        "Metafield: custom.target_market [single_line_text_field]":get(r,"market")})
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("-o","--out",default="shopify_products.csv")
    a=ap.parse_args(); rows=convert(load(a.input))
    w=csv.DictWriter(open(a.out,"w",newline="",encoding="utf-8-sig"),fieldnames=COLS); w.writeheader(); w.writerows(rows)
    print(f"✓ {len(rows)} 个产品 → {a.out}(Status=draft,待人审后在 Shopify 发布)")
if __name__=="__main__": main()
