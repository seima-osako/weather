require 'csv'
require 'mechanize'

agent = Mechanize.new
url = 'https://www.data.jma.go.jp/obd/stats/etrn/view/10min_s1.php?prec_no=44&block_no=47662&year=2019&month=01&day=01&view=p1'
page = agent.get(url)
html = page.search('tr')

out = []
html.each do |element|
    if element.get_attribute('style') == 'text-align:right;' then
        data_list=[]
        ele = element.search('td')
        ele.each do |e|
            data_list << e.inner_text
        end
        out << data_list
    end
end

header = ['時分','現地気圧','海面気圧','降水量','気温','相対湿度','平均風速','平均風向','最大瞬間風速','最大瞬間風向','日照時間']
CSV.open('tokyo_2019-01-01.csv','w') do |csv|
    csv << header
    out.each do |val|
        csv << val
    end        
end