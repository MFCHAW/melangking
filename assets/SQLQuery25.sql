declare @FY as int = 2024;
declare @Period as int = 5;

with temptbl as (
Select c.TransDetAPARKey, c.OUKey, i.Source, i.Type, i.RefCode, i.RefDesc, i.Amt, i.Qty, i.Rate   --b.docNum, d.TransDetKey, Format(d.Qty, '#,###.##') + ' MT, ' + Format((d.FuncTransAmt / d.Qty), '#,###.##') + ' RM/MT'
from FIN_TransDet a left join FIN_TransHdr b on a.TransHdrKey = b.TransHdrKey
		left join FIN_TransDet_APAR c on a.TransHdrKey = c.TransHdrKey and a.TransDetKey = c.TransDetKey
		left join FIN_TransDet d on c.APARRefTransHdrKey = d.TransHdrKey
		left join FIN_TransHdr e on d.TransHdrKey = e.TransHdrKey
		left join FPS_FinalPayDet f on f.FinalPayHdrKey = e.FinalPayHdrKey and f.FinalPayDetKey = d.FinalPayDetKey
		left join FPS_FFBApplyPaymentDet g on g.FFBApplyPaymentDetKey = f.FFBApplyPaymentDetKey
		left join FPS_FFBApplyPaymentHdr h on h.FFBApplyPaymentHdrKey = g.FFBApplyPaymentHdrKey
		left join FPS_ProformaFFBIncome i on i.FPSBatchKey = h.FPSBatchKey and i.ContactKey = g.ContactKey
Where b.FY = @FY and b.Period = @Period and b.Source = 'CRP' and b.DocType = 'BV' and b.OUKey = 1
		and b.GLDesc like 'FFB FINAL PAYMENT%' and a.Ind = 'V' and d.Ind = 'O'
		and i.RefCode <> 'FPSRDADJ'
UNION
Select c.TransDetAPARKey, c.OUKey, i.Source, i.Type, i.RefCode, i.RefDesc, i.Amt, i.Qty, i.Rate   --b.docNum, d.TransDetKey, Format(d.Qty, '#,###.##') + ' MT, ' + Format((d.FuncTransAmt / d.Qty), '#,###.##') + ' RM/MT'
from FIN_TransDet a left join FIN_TransHdr b on a.TransHdrKey = b.TransHdrKey
		left join FIN_TransDet_APAR c on a.TransHdrKey = c.TransHdrKey and a.TransDetKey = c.TransDetKey
		left join FIN_TransDet d on c.APARRefTransHdrKey = d.TransHdrKey
		left join FIN_TransHdr e on d.TransHdrKey = e.TransHdrKey
		left join FPS_FinalPayDet f on f.FinalPayHdrKey = e.FinalPayHdrKey and f.FinalPayDetKey = d.FinalPayDetKey
		left join FPS_FFBApplyPaymentDet g on g.FFBApplyPaymentDetKey = f.FFBApplyPaymentDetKey
		left join FPS_FFBApplyPaymentHdr h on h.FFBApplyPaymentHdrKey = g.FFBApplyPaymentHdrKey
		left join FPS_ProformaDeduction i on i.FPSBatchKey = h.FPSBatchKey and i.ContactKey = g.ContactKey
Where b.FY = @FY and b.Period = @Period and b.Source = 'CRP' and b.DocType = 'BV' and b.OUKey = 1
		and b.GLDesc like 'FFB FINAL PAYMENT%' and a.Ind = 'V' and d.Ind = 'O'
)
Select 'Invoice Amount: ' +
       Format((Select SUM(Rate)
	    From temptbl
		Where TransDetAPARKey = c.TransDetAPARKey and OUKey = c.OUKey 
		      and RefCode = 'FPSMTHPAY'), '#,###.00')
From FIN_TransDet a left join FIN_TransHdr b on a.TransHdrKey = b.TransHdrKey
	 left join FIN_TransDet_APAR c on a.TransHdrKey = c.TransHdrKey and a.TransDetKey = c.TransDetKey
	 left join FIN_TransDet d on c.APARRefTransHdrKey = d.TransHdrKey
Where b.FY = 2024 and b.Period = 5 and b.Source = 'CRP' and b.DocType = 'BV' and b.OUKey = 1
		and b.GLDesc like 'FFB FINAL PAYMENT%' and a.Ind = 'V' and d.Ind = 'O'






