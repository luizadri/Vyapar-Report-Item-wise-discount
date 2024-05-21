def send_purchase_report_via_mail(request):
  if request.method == 'POST':
    from_date_str=request.POST['fdate']
    To_date_str=request.POST['tdate']
    search=request.POST['search']
    filters_by=request.POST['filter']
    emails_string = request.POST['email']
    emails= [email.strip() for email in emails_string.split(',')]
    mess=request.POST['message']
    #filter using date-------------------
    if from_date_str and To_date_str:
      print(from_date_str)
      print(To_date_str)
      id=request.session.get('staff_id')
      staff=staff_details.objects.get(id=id)
      sales_data=SalesInvoiceItem.objects.filter(company=staff.company)
      distinct_items_with_discount = SalesInvoiceItem.objects.filter(company=staff.company).values('item__item_name').annotate(total_discount_amount=Sum('discount'),total_quantity=Sum('quantity'),total_sales_amount=Sum('totalamount'))
      content={
      'bill':purchase_data,
      'debit':debit_data,
      'staff':staff,
      'paid':paid,
      'unpaid':unpaid,
      'total':total,
      'sdate':from_date_str,
      'edate':To_date_str,
      'items_with_discount': distinct_items_with_discount
      }
      template_path = 'company/share_purchase_report_mail.html'
      template = get_template(template_path)

      html  = template.render(content)
      result = BytesIO()
      pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      pdf = result.getvalue()
      filename = f'Purchase Report.pdf'
      email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
      email.attach(filename, pdf, "application/pdf")
      email.send(fail_silently=False)
      messages.info(request,'purchase report shared via mail')
      return redirect('purchase_report')
    #if search input -------------------------
    if search:
      print(search)
      if PurchaseBill.objects.filter(billdate__startswith=search) or  purchasedebit.objects.filter(billdate__startswith=search):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,billdate__startswith=search).exists or purchasedebit.objects.filter(staff=id,billdate__startswith=search).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,billdate__startswith=search)
            debit_data=purchasedebit.objects.filter(staff=id,billdate__startswith=search)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')
      #party name---------------------
      if party.objects.filter(party_name__startswith=search):
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        party_name=party.objects.get(party_name__startswith=search)
        if PurchaseBill.objects.filter(staff=id,party=party_name.id).exists or purchasedebit.objects.filter(staff=id,party=party_name.id).exists:
          print('aa')
          purchase_data=PurchaseBill.objects.filter(staff=id,party=party_name.id)
          debit_data=purchasedebit.objects.filter(staff=id,party=party_name.id)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
          'bill':purchase_data,
          'debit':debit_data,
          'staff':staff,
          'paid':paid,
          'unpaid':unpaid,
          'total':total
          }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report') 
      if PurchaseBill.objects.filter(pay_method__istartswith=search):
        print(search)
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if PurchaseBill.objects.filter(staff=id,pay_method__istartswith=search).exists or purchasedebit.objects.filter(staff=id,payment_type__istartswith=search).exists:
          print('aa')
          purchase_data=PurchaseBill.objects.filter(staff=id,pay_method__istartswith=search)
          debit_data=purchasedebit.objects.filter(staff=id,payment_type__istartswith=search)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
          'bill':purchase_data,
          'debit':debit_data,
          'staff':staff,
          'paid':paid,
          'unpaid':unpaid,
          'total':total
          }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report')    
        # if enterd input is digit ------------------
      if search.isdigit():
        print(search)
        if PurchaseBill.objects.filter(billno__startswith=search) or  purchasedebit.objects.filter(billno__startswith=search):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,billno__startswith=search).exists or purchasedebit.objects.filter(staff=id,billno__startswith=search).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,billno__startswith=search)
            debit_data=purchasedebit.objects.filter(staff=id,billno__startswith=search)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')
          #grandtotal --------------------------    
        if PurchaseBill.objects.filter(grandtotal__startswith=search) or  purchasedebit.objects.filter(grandtotal__startswith=str(search)):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,grandtotal__startswith=search).exists or purchasedebit.objects.filter(staff=id,grandtotal__startswith=str(search)).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,grandtotal__startswith=search)
            debit_data=purchasedebit.objects.filter(staff=id,grandtotal__startswith=str(search))
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')    
          #balance--------------------------  
        if PurchaseBill.objects.filter(balance__startswith=search) or  purchasedebit.objects.filter(balance_amount__startswith=search):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,balance__startswith=search).exists or purchasedebit.objects.filter(staff=id,balance_amount__startswith=search).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,balance__startswith=search)
            debit_data=purchasedebit.objects.filter(staff=id,balance_amount__startswith=search)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
              'bill':purchase_data,
              'debit':debit_data,
              'staff':staff,
              'paid':paid,
              'unpaid':unpaid,
              'total':total
              }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report') 
      if search == 'bi' or search =='bil' or search =='bill' or search =='b':
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if PurchaseBill.objects.filter(staff=id).exists:
          purchase_data=PurchaseBill.objects.filter(staff=id)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
            'bill':purchase_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report') 
      if search == 'de' or search =='deb' or search =='debi' or search =='debit' or search =='debit n' or search =='debit note':
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if purchasedebit.objects.filter(staff=id).exists:
          debit_data=purchasedebit.objects.filter(staff=id)
          paid = unpaid = total=0
          # for i in purchase_data:
          #   paid +=float(i.advance)
          #   unpaid +=float(i.balance)
          #   total +=float(i.grandtotal)
          content={
            # 'bill':purchase_data,
            'debit':debit_data,
            # 'staff':staff,
            # 'paid':paid,
            # 'unpaid':unpaid,
            # 'total':total
            }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report')   
    if filters_by:
      print(filters_by)
      if PurchaseBill.objects.filter(billdate__startswith=filters_by) or  purchasedebit.objects.filter(billdate__startswith=filters_by):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,billdate__startswith=filters_by).exists or purchasedebit.objects.filter(staff=id,billdate__startswith=filters_by).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,billdate__startswith=filters_by)
            debit_data=purchasedebit.objects.filter(staff=id,billdate__startswith=filters_by)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')
      #party name---------------------
      if party.objects.filter(party_name__startswith=filters_by):
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        party_name=party.objects.get(party_name__startswith=filters_by)
        if PurchaseBill.objects.filter(staff=id,party=party_name.id).exists or purchasedebit.objects.filter(staff=id,party=party_name.id).exists:
          print('aa')
          purchase_data=PurchaseBill.objects.filter(staff=id,party=party_name.id)
          debit_data=purchasedebit.objects.filter(staff=id,party=party_name.id)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
          'bill':purchase_data,
          'debit':debit_data,
          'staff':staff,
          'paid':paid,
          'unpaid':unpaid,
          'total':total
          }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report') 
      if PurchaseBill.objects.filter(pay_method__istartswith=filters_by):
        print(filters_by)
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if PurchaseBill.objects.filter(staff=id,pay_method__istartswith=filters_by).exists or purchasedebit.objects.filter(staff=id,payment_type__istartswith=filters_by).exists:
          print('aa')
          purchase_data=PurchaseBill.objects.filter(staff=id,pay_method__istartswith=filters_by)
          debit_data=purchasedebit.objects.filter(staff=id,payment_type__istartswith=filters_by)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
          'bill':purchase_data,
          'debit':debit_data,
          'staff':staff,
          'paid':paid,
          'unpaid':unpaid,
          'total':total
          }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report')    
        # if enterd input is digit ------------------
      if search.isdigit():
        print(search)
        if PurchaseBill.objects.filter(billno__startswith=filters_by) or  purchasedebit.objects.filter(billno__startswith=filters_by):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,billno__startswith=filters_by).exists or purchasedebit.objects.filter(staff=id,billno__startswith=filters_by).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,billno__startswith=filters_by)
            debit_data=purchasedebit.objects.filter(staff=id,billno__startswith=filters_by)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')
          #grandtotal --------------------------    
        if PurchaseBill.objects.filter(grandtotal__startswith=filters_by) or  purchasedebit.objects.filter(grandtotal__startswith=str(filters_by)):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,grandtotal__startswith=filters_by).exists or purchasedebit.objects.filter(staff=id,grandtotal__startswith=str(filters_by)).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,grandtotal__startswith=filters_by)
            debit_data=purchasedebit.objects.filter(staff=id,grandtotal__startswith=str(filters_by))
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
            'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report')    
          #balance--------------------------  
        if PurchaseBill.objects.filter(balance__startswith=filters_by) or  purchasedebit.objects.filter(balance_amount__startswith=filters_by):
          id=request.session.get('staff_id')
          staff=staff_details.objects.get(id=id)
          if PurchaseBill.objects.filter(staff=id,balance__startswith=filters_by).exists or purchasedebit.objects.filter(staff=id,balance_amount__startswith=filters_by).exists:
            purchase_data=PurchaseBill.objects.filter(staff=id,balance__startswith=filters_by)
            debit_data=purchasedebit.objects.filter(staff=id,balance_amount__startswith=filters_by)
            paid = unpaid = total=0
            for i in purchase_data:
              paid +=float(i.advance)
              unpaid +=float(i.balance)
              total +=float(i.grandtotal)
            content={
              'bill':purchase_data,
              'debit':debit_data,
              'staff':staff,
              'paid':paid,
              'unpaid':unpaid,
              'total':total
              }
            template_path = 'company/share_purchase_report_mail.html'
            template = get_template(template_path)

            html  = template.render(content)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            pdf = result.getvalue()
            filename = f'Purchase Report.pdf'
            email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
            email.attach(filename, pdf, "application/pdf")
            email.send(fail_silently=False)
            messages.info(request,'purchase report shared via mail')
            return redirect('purchase_report') 
      if filters_by == 'bi' or filters_by =='bil' or filters_by =='bill' or filters_by =='b':
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if PurchaseBill.objects.filter(staff=id).exists:
          purchase_data=PurchaseBill.objects.filter(staff=id)
          paid = unpaid = total=0
          for i in purchase_data:
            paid +=float(i.advance)
            unpaid +=float(i.balance)
            total +=float(i.grandtotal)
          content={
            'bill':purchase_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report') 
      if filters_by == 'de' or filters_by =='deb' or filters_by =='debi' or filters_by =='debit' or filters_by =='debit n' or filters_by =='debit note':
        id=request.session.get('staff_id')
        staff=staff_details.objects.get(id=id)
        if purchasedebit.objects.filter(staff=id).exists:
          debit_data=purchasedebit.objects.filter(staff=id)
          paid = unpaid = total=0
          for i in debit_data:
            paid +=float(i.paid_amount)
            unpaid +=float(i.balance_amount)
            total +=float(i.grandtotal)
          content={
            # 'bill':purchase_data,
            'debit':debit_data,
            'staff':staff,
            'paid':paid,
            'unpaid':unpaid,
            'total':total
            }
          template_path = 'company/share_purchase_report_mail.html'
          template = get_template(template_path)

          html  = template.render(content)
          result = BytesIO()
          pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
          pdf = result.getvalue()
          filename = f'Purchase Report.pdf'
          email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
          email.attach(filename, pdf, "application/pdf")
          email.send(fail_silently=False)
          messages.info(request,'purchase report shared via mail')
          return redirect('purchase_report')   
    if search == '' or filters_by == '' or from_date_str == '' or To_date_str == '' :
      id=request.session.get('staff_id')
      staff=staff_details.objects.get(id=id)
      purchase_data=PurchaseBill.objects.filter(staff=id)
      debit_data=purchasedebit.objects.filter(staff=id)
      paid = unpaid = total=0
      for i in purchase_data:
        paid +=float(i.advance)
        unpaid +=float(i.balance)
        total +=float(i.grandtotal)
      content={
        'bill':purchase_data,
        'debit':debit_data,
        'staff':staff,
        'paid':paid,
        'unpaid':unpaid,
        'total':total
      }
      template_path = 'company/share_purchase_report_mail.html'
      template = get_template(template_path)
      html  = template.render(content)
      result = BytesIO()
      pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      pdf = result.getvalue()
      filename = f'Purchase Report.pdf'
      email = EmailMessage(mess,from_email=settings.EMAIL_HOST_USER,to=emails)
      email.attach(filename, pdf, "application/pdf")
      email.send(fail_silently=False)
      messages.info(request,'purchase report shared via mail')
      return redirect('purchase_report') 
  return redirect('purchase_report')  