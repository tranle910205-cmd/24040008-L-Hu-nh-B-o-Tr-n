from pathlib import Path
import html
import re

ROOT = Path(__file__).parent
esc = html.escape
NAV = [('index.html','Trang chủ'),('business-plan.html','Kế hoạch kinh doanh'),('financial-analysis.html','Tài chính'),('swot.html','SWOT'),('five-forces.html','5 áp lực cạnh tranh'),('reflections.html','Phản hồi đọc sách'),('action-plan.html','Kế hoạch 90 ngày')]

def page(file, title, lead, content, category='HỒ SƠ DỰ ÁN'):
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == file or (file.startswith('reflection-') and url == 'reflections.html') else '')+f'>{label}</a>' for url,label in NAV)
    output = f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(lead)}"><title>{esc(title)} · Hồ sơ khởi nghiệp</title><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Đến nội dung chính</a><header><div class="header-inner"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">↗</span><span>HỒ SƠ KHỞI NGHIỆP<small>Ý tưởng · Phân tích · Hành động</small></span></a><nav aria-label="Điều hướng chính">{nav}</nav></div></header>
<main id="main"><section class="page-heading"><p class="eyebrow">{category}</p><h1>{esc(title)}</h1><p class="lead">{esc(lead)}</p></section>{content}</main><footer><span>Hồ sơ dự án khởi nghiệp</span><a href="reflections.html">Thư viện phản hồi đọc sách ↗</a><span>Nội dung từ tài liệu Markdown của dự án.</span></footer></body></html>'''
    (ROOT/file).write_text(output, encoding='utf-8')

NOTICE = '<aside class="notice"><span class="notice-icon" aria-hidden="true">i</span><div><strong>Chưa có tài liệu kế hoạch kinh doanh</strong><p>Không tìm thấy tệp <code>business_plan.md</code>. Mục <code>Business-plan.md</code> hiện là thư mục chứa các bản sao bài phản hồi. Nội dung kinh doanh đang chờ nguồn chính thức.</p></div></aside>'

def empty(title, text, symbol='↗'):
    return f'<article class="card empty"><span class="tile-icon" aria-hidden="true">{symbol}</span><h2>{title}</h2><p>{text}</p><span class="status">Chờ tài liệu nguồn</span></article>'

summaries = {
'Lê Huỳnh Bảo Trân':'Bảo Trân nhấn mạnh việc chủ động thích nghi với AI, sử dụng công nghệ đúng mục đích và kiểm chứng thông tin. Tư duy sáng tạo, khả năng học hỏi liên tục và vai trò chủ động của con người là những bài học nổi bật.',
'Lê Hoàng Trà My':'Trà My nhìn nhận AI như một cộng sự hỗ trợ tư duy, sáng tạo và lập kế hoạch. Bài phản hồi nhấn mạnh việc giữ tư duy phản biện, cảm xúc và bản sắc cá nhân, đồng thời chịu trách nhiệm với sản phẩm cuối cùng.',
'Lâm Quỳnh Như':'Quỳnh Như liên hệ AI với ngành Quan hệ công chúng, từ ý tưởng đến kế hoạch truyền thông. Bài viết đề cao tư duy chiến lược, kiểm chứng thông tin, quyền riêng tư và việc làm chủ AI một cách có trách nhiệm.',
'Lợi Ngọc Bảo Châu':'Bảo Châu nhận ra giới hạn của AI và nguy cơ quá tin vào kết quả máy tính. Từ góc nhìn sinh viên Truyền thông số, bài viết nhấn mạnh tư duy phản biện, chọn lọc thông tin và sáng tạo độc lập.',
'Phạm Nguyễn Diễm Quỳnh':'Diễm Quỳnh xem AI là người đồng hành giúp mở rộng năng lực, đồng thời nhấn mạnh trách nhiệm định hướng và kiểm soát của con người. Bài viết liên hệ các ứng dụng với ngành PR và đề cao tư duy, đạo đức cùng sự thấu hiểu công chúng.'
}

def inline(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

def markdown(text):
    blocks=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        lines=block.splitlines()
        if all(line.startswith('- ') for line in lines):
            blocks.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in lines)+'</ul>')
        elif lines[0].startswith('#'):
            match=re.match(r'^(#{1,6})\s+(.+)',lines[0])
            level=min(len(match[1])+1,6)
            blocks.append(f'<h{level}>'+inline(match[2])+f'</h{level}>')
        else:
            blocks.append('<p>'+'<br>'.join(inline(line) for line in lines)+'</p>')
    return '\n'.join(blocks)

cards=[]
for i,source in enumerate(sorted((ROOT/'Reflections').glob('*.md')),1):
    text=source.read_text(encoding='utf-8')
    name=re.search(r'^Họ và tên:\s*(.+)$',text,re.M)[1].strip()
    book=re.search(r'^Tên sách:\s*(.+)$',text,re.M)[1].strip()
    author=re.search(r'^Tác giả:\s*(.+)$',text,re.M)[1].strip()
    file=f'reflection-{i:02}.html'
    source_url=esc(source.relative_to(ROOT).as_posix(),quote=True)
    initials=''.join(part[0] for part in name.split()[-2:])
    cards.append(f'<article class="card member"><div class="member-head"><span class="avatar">{initials}</span><span class="tag">Phản hồi đọc sách</span></div><h2>{esc(name)}</h2><h3>{esc(book)}</h3><p class="muted">Tác giả: {esc(author)}</p><p>{summaries[name]}</p><div class="card-bottom"><a class="text-link" href="{file}">Đọc toàn bộ bài phản hồi <span aria-hidden="true">↗</span></a><a class="source-link" href="{source_url}">Tệp Markdown gốc</a></div></article>')
    # Student numbers are omitted from public pages; retain the student's actual prose.
    body=re.sub(r'^#\s+\d+\s*\n','',text,count=1)
    content=f'<div class="reading-layout"><aside class="reading-aside"><a class="text-link" href="reflections.html">← Tất cả bài phản hồi</a><div class="book-label">CUỐN SÁCH</div><h2>{esc(book)}</h2><p>{esc(author)}</p><a class="button secondary" href="{source_url}">Mở Markdown gốc ↗</a></aside><article class="prose">{markdown(body)}</article></div>'
    page(file,name,'Bài phản hồi đọc sách của thành viên.',content,'THƯ VIỆN / PHẢN HỒI ĐỌC SÁCH')

page('reflections.html','Những góc nhìn từ trang sách','Mỗi thành viên, một góc nhìn riêng về trí tuệ nhân tạo, học tập và nghề nghiệp.','<div class="section-label"><h2>Phản hồi đọc sách của thành viên</h2><span>Nguồn: Reflections/</span></div><div class="grid members">'+''.join(cards)+'</div>','THƯ VIỆN THÀNH VIÊN')

home='<section class="hero-panel"><div><p class="eyebrow">TỪ Ý TƯỞNG ĐẾN HÀNH ĐỘNG</p><h2>Khám phá dự án.<br>Hiểu từng góc nhìn.</h2><p>Không gian tổng hợp kế hoạch kinh doanh, các phân tích và phản hồi đọc sách của thành viên.</p><div class="actions"><a class="button" href="reflections.html">Khám phá bài phản hồi ↗</a><a class="button secondary light" href="business-plan.html">Kế hoạch kinh doanh</a></div></div><div class="hero-art" aria-hidden="true"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><span class="art-center">↗</span><span class="art-label">Ý TƯỞNG</span><span class="art-label second">HÀNH ĐỘNG</span></div></section>'
home+=NOTICE+'<section><div class="section-label"><h2>Khám phá hồ sơ</h2><span>Đi từ tổng quan đến chi tiết</span></div><div class="grid overview">'
descriptions=['Mô hình và định hướng của dự án.','Các chỉ số và cơ cấu tài chính.','Điểm mạnh, điểm yếu, cơ hội và thách thức.','Năm góc nhìn về môi trường cạnh tranh.','Bài viết riêng và cảm nhận của từng thành viên.','Lộ trình triển khai và các mốc hành động.']
for (url,label),desc in zip(NAV[1:],descriptions):
    home+=f'<a class="card destination" href="{url}"><span class="tile-icon" aria-hidden="true">↗</span><h2>{label}</h2><p>{desc}</p><span class="text-link">'+('Đọc các bài phản hồi' if url=='reflections.html' else 'Chờ nguồn kinh doanh')+' →</span></a>'
home+='</div></section>'
page('index.html','Hồ sơ dự án khởi nghiệp','Kế hoạch, phân tích và góc nhìn của thành viên trong một không gian.',home)
page('business-plan.html','Kế hoạch kinh doanh','Nguồn chính thức cho định hướng và toàn bộ nội dung kinh doanh của dự án.',NOTICE+empty('Nội dung đang chờ nguồn','Kế hoạch kinh doanh sẽ được trình bày khi có tệp business_plan.md.'))
page('financial-analysis.html','Phân tích tài chính','Các chỉ số tài chính được trình bày theo số liệu trong kế hoạch kinh doanh.',NOTICE+'<div class="grid">'+empty('Chỉ số tài chính','Chưa có số liệu nguồn để hiển thị KPI.','₫')+empty('Trực quan hóa tài chính','Chưa có dữ liệu để vẽ biểu đồ tài chính.','▥')+'</div>')
swot=[('S','Điểm mạnh · Strengths'),('W','Điểm yếu · Weaknesses'),('O','Cơ hội · Opportunities'),('T','Thách thức · Threats')]
page('swot.html','Phân tích SWOT','Bốn nhóm yếu tố được tách riêng để theo dõi rõ ràng.',NOTICE+'<div class="grid swot">'+''.join(empty(title,'Chưa có nội dung SWOT từ kế hoạch kinh doanh.',symbol) for symbol,title in swot)+'</div>')
forces=['Mức độ cạnh tranh trong ngành','Nguy cơ từ đối thủ mới gia nhập','Quyền thương lượng của nhà cung cấp','Quyền thương lượng của khách hàng','Nguy cơ từ sản phẩm hoặc dịch vụ thay thế']
page('five-forces.html','5 áp lực cạnh tranh của Porter','Năm yếu tố cạnh tranh được trình bày riêng theo kế hoạch kinh doanh.',NOTICE+'<div class="grid forces">'+''.join(empty(title,'Chưa có nội dung từ business_plan.md để trình bày yếu tố này.',f'{i:02}') for i,title in enumerate(forces,1))+'</div>')
page('action-plan.html','Kế hoạch hành động 90 ngày','Lộ trình hành động và các mốc triển khai từ kế hoạch kinh doanh.',NOTICE+empty('Lộ trình đang chờ nguồn','Chưa có giai đoạn, thời điểm hoặc công việc từ nguồn chính thức để dựng timeline.','→'))
print('Created 12 HTML pages; each reflection links to its own Markdown source.')
