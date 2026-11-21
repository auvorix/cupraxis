# 03 — RF e antenas: posicionamento, linhas de 50 Ω, casamento, blindagem, coexistência, conectores e conformidade

> Pesquisa de 2026-11-20 para o corpus da skill "especialista em PCB" (KiCad 10, JLCPCB, produtos vendidos na UE com Wi-Fi/BLE 2,4/5 GHz, sub-GHz CC1101, GNSS, nRF24).
> PDFs baixados: `boas-praticas\pdfs\03-rf\` (lista e licenças em `pdfs\03-rf\LICENSES.md`).
> **Não duplica** `referencias\rf-reference-designs\`: a rede de casamento do CC1101 (DN017 + CC1101EM 434 MHz), a entrada RF do MAX-M10S (manual de integração UBX-20053088) e o nRF24L01 (product spec) estão lá e são só referenciados aqui.
> Etiquetas: **FATO** = conferido na fonte lida (PDF baixado ou página aberta); **INFERÊNCIA** = dedução minha, conta minha, prática comum sem fonte primária, ou dado que só vi em resultado de busca e não consegui abrir na fonte.
> Citações abreviadas (ex.: "TI AN058 §3.4", "NINA-B3 SIM", "u-blox UBX-15030289 §6.3") remetem à URL completa listada na **Bibliografia**.

---

## Resumo executivo

1. **Use módulo certificado com antena impressa sempre que der** (ESP32-C5/S3/C3-WROOM/MINI, módulos nRF52 tipo NINA-B3). O layout se resume a cumprir o *keepout* (área livre) do fabricante: antena **para fora da borda** ou com o ponto de alimentação/GND **na borda/canto**, placa base **cortada** sob a antena e dos lados, **nada de cobre em nenhuma camada** sob a antena, e **≥ 15 mm de folga até a carcaça** (Espressif). Na UE, isso também permite reaproveitar a avaliação de rádio (art. 3.2) e de EMC do módulo, desde que ele seja instalado conforme as instruções e o caminho de RF não seja alterado (ETSI EG 203 367 §5–6).
2. **Linha de 50 Ω na JLCPCB = 4 camadas.** A página de capacidades da JLCPCB lista impedância controlada (±10 %) para **4/6/8… camadas**; 2 camadas não aparece na lista (não está escrito "só", mas não é oferecido) — conferido em 2026-11-20. No `JLC04161H-7628` (L1 sobre 0,2104 mm de 7628, εr 4,4) a **CPWG** fica em **W ≈ 0,30 mm com gap ≈ 0,30 mm** (contas abaixo, validadas com o empilhamento publicado pela Espressif e com a calculadora da JLC). A microstrip pura dá W ≈ 0,36 mm. Em 2 camadas de 1,6 mm a CPWG é possível (W 0,69 mm com gap 0,20 mm), mas o **gap domina**: ±0,05 mm no gap muda Z de 43 para 55 Ω, e a fábrica não testa a impedância.
3. **Rede de casamento:** ponha a rede CLC/π **colada no pino do chip** (componentes 0201, ou 0402 C0G) e uma **segunda π perto da antena ou do conector**, com 0 Ω/DNP de fábrica. A Espressif avisa que os valores dos módulos **não se transferem** para outra placa: é preciso ajustar com VNA (S11 ≈ conjugado do chip, harmônicas S21 < −35 dB).
4. **Vias de costura:** dimensione o passo pela **maior frequência fundamental** e pelo **comprimento de onda na placa**. Com λ/20 e εeff ≈ 3,3 dá **≈ 3,4 mm a 2,45 GHz**, **≈ 1,4 mm a 5,85 GHz**, **≈ 9,5 mm a 868 MHz** e **≈ 19 mm a 433 MHz**. **Atualização 2026-11-21 (`12`):** para cerca e costura, calcule com o εr do FR-4 (≈ 4,4), porque a onda bloqueada viaja no dielétrico: ≈ 2,9 mm a 2,45 GHz, ≈ 1,2 mm a 5,8 GHz, ≈ 8,2 mm a 868 MHz, ≈ 16 mm a 433 MHz. Coloque cerca dos dois lados de toda CPWG (Silicon Labs) e anel de vias sob a moldura de blindagem.
5. **Coexistência:** Wi-Fi a +20 dBm exige **45–50 dB** de isolamento entre antenas para não surdar BLE/802.15.4, mas produtos pequenos conseguem **15–20 dB** (Silicon Labs). A distância sozinha dá pouco: a 2,45 GHz e 100 mm são ≈ 20 dB de perda de espaço livre, menos o ganho das antenas. Portanto, nRF24 + Wi-Fi na mesma placa pedem **coordenação no tempo e no canal**, além de afastamento e orientação.
6. **GNSS:** o receptor é o mais sensível. Mantenha-o longe de SMPS, USB 3, clocks e transmissores. Use SAW se houver transmissor forte. Antena passiva só com microstrip ≤ 10 cm; acima disso use antena ativa com LNA de 15–26 dB e *bias tee* (u-blox).
7. **Conectores:** prefira SMA de borda (edge) no plano de terra alinhado, com o pad do sinal até a borda. Sob o pad central de SMA/u.FL, abra o GND (pelo menos na 1ª camada interna). Em produto Wi-Fi/BT o padrão de fato é RP-SMA, para dificultar a troca por antena de ganho maior (u-blox).

---

## Regras acionáveis

### A. Posicionamento de antenas

**A.1 Módulos com antena impressa (ESP32-C5/S3/C3, nRF52 tipo NINA-B3)**

1. **Antena do módulo para fora da placa base, ou com o ponto de alimentação/GND na borda.** Se a antena não puder sair da borda, **corte a placa base sob a antena e dos dois lados**. **Nunca** ponha o módulo no meio da placa com um recorte nos 4 lados.
   **Por quê:** o material e o cobre da placa base desintonizam a antena. — FATO, Espressif ESP32-C5 HW Design Guidelines §1.4.7 (o mesmo texto aparece nos guias do C3 e do S3): https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/esp-hardware-design-guidelines-en-master-esp32c5.pdf
2. **Keepout do módulo ESP32-C5** (fig. 23, unidade mm): área livre de **≥ 15 mm** ao lado da antena, ao longo da borda, e **6,5 mm** de profundidade. A antena fica rente à borda, com as cotas "Max 2" e "Max 1" entre a antena e o contorno da placa. Ponha **GND e vias densas na placa base perto da antena**.
   **Por quê:** é a área em que a antena foi caracterizada. — FATO (leitura da figura e do texto), mesmo PDF.
3. **≥ 15 mm de folga em todas as direções entre a antena impressa e a carcaça.** Depois, teste vazão e alcance no produto final. — FATO, Espressif C5/C3/S3 §1.4.7 ("A clearance of at least 15 mm is recommended in all directions").
4. **NINA-B3 (nRF52840), regras do fabricante:**
   - **NINA-B3x2 (antena interna):** módulo **no canto**, com o ponto de alimentação no canto. Outras posições na borda funcionam com desempenho "moderadamente reduzido". **GND cheio sob todo o módulo, inclusive sob a antena** (exceção à regra geral: é o que este fabricante pede).
   - **NINA-B3x6 (antena de trilha):** módulo **no centro de uma borda**, com GND estendendo-se **≥ 10 mm de cada lado** e recorte de GND sob a antena conforme a figura 14 do manual.
   - **Peças altas/metálicas a ≥ 10 mm da antena.**
   - **Folga até a carcaça ≥ 5 mm (B3x2) ou ≥ 10 mm (B3x6)**. PC e ABS desintonizam menos, POS desintoniza mais.
   — FATO, u-blox NINA-B3 System Integration Manual UBX-17056748 R15, "Antenna integration": https://content.u-blox.com/sites/default/files/NINA-B3_SIM_UBX-17056748.pdf
5. **Siga sempre o keepout do datasheet do módulo exato.** Os fabricantes divergem (por exemplo, GND sob a antena no NINA-B3x2 contra recorte no ESP e no NINA-B3x6). Não generalize de um módulo para outro. — INFERÊNCIA (comparação das duas fontes acima).
6. **Metal externo a ≥ 15 mm da antena cerâmica**, e **nenhum cobre (top, camadas internas ou bottom) sob a antena**. — FATO, Microchip BM20/23, §4.2 Module Placement Rules: https://onlinedocs.microchip.com/oxy/GUID-26060FFF-4EA0-483D-BCBB-39AF46A5A76C-en-US-6/GUID-3351AEE9-DDD5-4583-8492-53634B5FD77C.html
7. **Mantenha longe da antena:** USB, conversor USB-serial, linhas UART (trilhas, vias, test points, headers), cristais, DDR e clocks rápidos. Contorne a UART com GND e vias. Se o TX vai bem e o RX vai mal, o culpado costuma ser o acoplamento de harmônicas (por exemplo, do cristal) na antena. — FATO, Espressif C5 §1.4.4 e §1.4.10 (Typical Layout Problems and Solutions).

**A.2 Antenas de PCB (inverted-F/IFA, meandro, monopolo) e plano de terra**

8. **Copie a antena de referência exatamente**: importe o DXF/Gerber do fabricante e sobreponha os Gerbers para conferir. Use a **mesma espessura e o mesmo material** da referência. Para compensar placa mais grossa/fina, encurte/alongue um pouco a antena. — FATO, TI AN043 (SWRA117D) §4.3 e TI DN007 (SWRU120): https://www.ti.com/lit/an/swra117d/swra117d.pdf · https://www.ti.com/lit/an/swru120d/swru120d.pdf
9. **Referências TI prontas** (todas FATO, nos PDFs citados):
   | Antena | Faixa | Área | Placa de referência | Ganho máx. |
   |---|---|---|---|---|
   | DN007 IFA | 2,4 GHz | 25,7 × 7,5 mm (fora o GND) | FR-4 de **1,0 mm** | +3,3 dBi |
   | AN043 IFA "USB dongle" | 2,4 GHz | 15,2 × 5,7 mm | ver *readme* do projeto CC2511 | 5,3 dB (XZ) |
   | DN023 IFA | 868/915/955 MHz | 43 × 20 mm | FR-4 de **0,8 mm** | −0,12 dB |
   Para comparar: λ/4 no ar = 3,1 cm a 2,4 GHz, 8,6 cm a 868 MHz e 17,3 cm a 433 MHz (TI AN058, tabela 1).
10. **Sem GND, trilhas nem componentes sob a antena.** No DN023, **≥ 5 mm** livres de cada lado da antena. — FATO, TI AN058 (SWRA161B) §7 ("No ground plane or traces should be placed beneath the antenna") e DN023 §3.1: https://www.ti.com/lit/an/swra161b/swra161b.pdf · https://www.ti.com/lit/an/swra228c/swra228c.pdf
11. **Monopolo impresso Nordic (~23 mm a 2,4 GHz): ≥ 5 mm de folga até o plano de GND.** — FATO, Nordic DevZone "General PCB design guidelines for nRF52" (a própria página avisa que **não é mantida**): https://devzone.nordicsemi.com/guides/hardware-design-test-and-measuring/b/nrf5x/posts/general-pcb-design-guidelines-for-nrf52-series
12. **Comprimento mínimo do plano de GND ≈ λ/4 da menor frequência irradiada**, e quanto maior, melhor a eficiência. Contas (INFERÊNCIA, λ/4 no ar): ≈ 31 mm a 2,4 GHz, ≈ 86 mm a 868 MHz, ≈ 173 mm a 433 MHz. Em placa pequena de sub-GHz, o GND fica abaixo de λ/4 e a antena perde eficiência: use antena de fio/helicoidal ou SMA externa. — FATO para a regra, NINA-B3 SIM ("may be reduced to a minimum size that is similar to one quarter of wavelength of the minimum frequency").
13. **O tamanho e o formato do GND mudam casamento e diagrama.** Plugar a placa em outra (por exemplo, USB no notebook) muda a antena. No AN043, a banda caiu de ~250 MHz para ~100 MHz com o dongle no laptop. — FATO, TI AN058 §5 e AN043 §4.3.
14. **Plástico desloca a ressonância para baixo**, e a mão degrada ainda mais. Antena com banda larga (IFA com > 300 MHz a 10 % de reflexão) tolera melhor. Preveja ajuste (encurtar a antena ou mexer na π). — FATO, TI AN043 §4.3, DN007 §2.2 e AN058 §6.
15. **Placa que pluga num host (módulo de expansão, HAT, shield, dongle):** o GND do host muda quando a placa é plugada. Afine a π **com o módulo plugado no host e dentro da carcaça**. — INFERÊNCIA (aplicação direta da regra 13).

**A.3 Antenas chip (cerâmica)**

16. **O casamento do datasheet vale só para a placa de avaliação** (tamanho e forma do GND). Na sua placa quase sempre serão precisos componentes extras. — FATO, TI AN058 §4.2; Johanson "Chip Antenna Layout Considerations for 802.11" (2006): https://johansontechnology.com/docs/2/jti-antenna-mounting.pdf
17. **Johanson, folgas típicas:** **> 2 mm** dos lados curtos até o GND (ou > 1 mm do lado curto mais próximo, no arranjo alternativo) e **> 4 mm** do lado longo, com a antena na borda da placa. A **microstrip que alimenta a antena faz parte do sistema ressonante**. Costure a borda do GND em volta da linha com muitas vias. Com GND de ~3–4 cm × 1–2 cm, o sistema se comporta como dipolo. — FATO, mesmo PDF.
18. **Kyocera AVX 1001013 (2,4 GHz):**
    - antena **sempre na borda**, com o ponto de alimentação a **5–15 mm do canto**, numa borda **≥ 50 mm**;
    - a folga de GND é "o fator mais crítico": até **2 dB** de diferença entre fora do GND e sobre o GND;
    - a placa de demonstração tem 72 × 50 mm com 5,70 mm de folga;
    - vias de 0,2 mm, **nunca na linha de transmissão**.
    — FATO, AVX-E AppNote 1001013: https://www.kyocera-avx.com/docs/techinfo/ApplicationNotes/Antenna-AppNotes/AVX-E_AppNote-1001013.pdf
19. **Antenas "booster" (Ignion/Fractus mXTEND)** pedem **canto da placa** e área livre do manual (por exemplo, ONE mXTEND 30 × 8 mm na placa de avaliação). — INFERÊNCIA: só vi o trecho indexado do manual; o PDF da Mouser bloqueou o download. Confirme no manual do PN.

**A.4 Orientação e polarização**

20. **Antena e receptor devem ter a mesma polarização**, mas em ambiente interno os reflexos tornam isso menos crítico. — FATO, TI AN058 §5.1.1.
21. **Use o nulo do monopolo:** aponte o eixo do monopolo para a outra antena (por exemplo, a de Wi-Fi) para ganhar isolamento. — FATO, Silicon Labs "Unmanaged Coexistence": https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/03-unmanaged-coexistence
22. **Antenas de bandas iguais lado a lado devem ser ortogonais (polarização cruzada)** e o mais afastadas possível. — INFERÊNCIA (prática comum, sem número de fonte primária).

### B. Linhas de transmissão de 50 Ω

**B.0 Memória de cálculo** (script em Python, conformal mapping de CPWG de Ghione/Wadell com correção de espessura de Gupta; microstrip de Hammerstad–Jensen).

- **CPWG** (GND lateral + plano abaixo): k = W/(W+2S), k₁ = tanh(πW/4h)/tanh(π(W+2S)/4h).
  - εeff = [1 + εr·(K(k′)/K(k))·(K(k₁)/K(k₁′))] / [1 + (K(k′)/K(k))·(K(k₁)/K(k₁′))]
  - Z₀ = 60π / √εeff · 1/[K(k)/K(k′) + K(k₁)/K(k₁′)]
  - Espessura t: W += Δ e S −= Δ, com Δ = (1,25t/π)(1 + ln(4πW/t)).
- **Sem máscara de solda no modelo.** A máscara baixa um pouco o Z, então a calculadora da JLC (que considera máscara) pode pedir trilha um pouco mais estreita. — INFERÊNCIA.
- **Validação 1 (FATO de entrada):** a Espressif publica, para o C5, CPWG de **W 12,6 mil / gap 12,2 mil** sobre **7628 de 8,22 mil, Dk 4,6**, cobre acabado de 0,8 mil, como 50 Ω (fig. 17). O meu modelo dá **50,3 Ω** com t = 0,8 mil, ou 47,7 Ω com t = 35 µm.
- **Validação 2:** numa pergunta no help center da JLC, um usuário mostra a saída da calculadora para 2 camadas, 1,6 mm, 1 oz: CPWG com **gap 30 mil → W 83 mil**, e microstrip sem GND lateral → 107 mil. O meu modelo dá **82 mil** para gap 30 mil. Fonte: https://jlcpcb.com/help/answers/detail/331-Coplanar-and-non-coplanar-Impedance-calculator (FATO quanto ao texto; é pergunta de usuário, sem resposta oficial).

**Tabela 1 — JLC04161H-7628, L1 sobre L2.** Entradas: h = 0,2104 mm (7628×1), εr 4,4, cobre externo de 0,035 mm (FATO, página de stackups da JLC: https://jlcpcb.com/impedance). Os resultados são INFERÊNCIA (conta minha, ±~5 %).

| Estrutura | gap S (mm) | W para 50 Ω (mm) | εeff |
|---|---|---|---|
| Microstrip (sem GND lateral) | — | **0,365** | 3,33 |
| CPWG | 0,15 | 0,217 | 2,94 |
| CPWG | 0,20 | 0,262 | 3,05 |
| CPWG | 0,25 | 0,287 | 3,13 |
| **CPWG (recomendado)** | **0,30** | **0,303** | 3,19 |

Conferência: a geometria da Espressif (W 0,32 / S 0,31 mm) no stackup da JLC dá 48,8 Ω, e W 0,30 / S 0,30 dá 50,2 Ω.

**Tabela 2 — 2 camadas, 1,6 mm.** Entradas: dielétrico ≈ 1,51 mm (assumido: 1,6 mm menos o cobre), εr 4,5 (FATO, JLC Capabilities: "4.5 (2-Layer PCB)"), t = 0,035 mm. Resultados INFERÊNCIA.

| Estrutura | gap S (mm) | W para 50 Ω (mm) |
|---|---|---|
| Microstrip | — | **2,79** (a JLC fala em ~2,8–3 mm) |
| CPWG | 0,15 | 0,42 |
| CPWG | 0,20 | 0,69 |
| CPWG | 0,25 | 0,93 |
| CPWG | 0,30 | 1,14 |
| CPWG | 0,762 (30 mil) | 2,08 (calculadora JLC: 2,11) |

Sensibilidade (INFERÊNCIA): com W = 0,69 mm, gap 0,15 dá **43,4 Ω** e gap 0,25 dá **54,9 Ω**. Em 2 camadas é o gap, ou seja, a tolerância de corrosão, que manda.

**B.1 Regras**

23. **Em 50 Ω controlado na JLCPCB, use 4 camadas.** Impedância controlada só existe para **4/6/8… camadas**, com tolerância **±10 %**. Em 2 camadas a placa sai, mas sem controle nem teste. — FATO, https://jlcpcb.com/capabilities/Capabilities
24. **Prefira CPWG (coplanar com GND) a microstrip pura** em placa densa: a linha fica mais estreita, o campo fica confinado e dá para fazer cerca de vias. Silicon Labs: "A coplanar waveguide… is recommended" e "A via fence is recommended on both sides". Nordic: linha "should be a coplanar waveguide". — FATO: https://docs.silabs.com/z-wave/8.0.0/z-wave-800-series-integration-guide/08-pcb-implementation e Nordic DevZone (acima).
25. **Referência = a camada logo abaixo** (L2 GND sólido). **Não passe nada sob a trilha de RF.** A Espressif pede L2 sem trilhas e L3 com GND sob RF e cristal. — FATO, Espressif C5 §1.4.1 e §1.4.4.
26. **Trilha de RF só na camada externa, sem vias e sem ramificações**, com largura constante, curta e cercada de vias de GND densas. Curvas a **135° (chanfro de 45°) ou em arco**. — FATO, Espressif C5 §1.4.4; NINA-B3 SIM ("route RF lines in 45° angle or in arcs").
26a. **Se a troca de camada for inevitável** (por exemplo, conector no bottom), ponha **vias de retorno de GND logo ao lado da via de sinal** (par de vias de GND em cada transição) e mantenha o antipad coerente com 50 Ω. — INFERÊNCIA, por analogia com a regra da Espressif para USB ("add a pair of ground return vias at each transition point", C5 §1.4.8). O preferível continua sendo não trocar de camada (regra 26).
27. **Largura ≥ 200 µm** para controlar bem a impedância no processo da fábrica. Peça à fábrica o valor final e, se possível, um cupom de impedância. — FATO, NINA-B3 SIM. A tabela 1 (0,30 mm) cumpre.
28. **Quando a trilha precisa ser tratada como linha de 50 Ω:** acima de **λ/16** da fundamental (Silicon Labs, FATO). Contas (INFERÊNCIA, εeff 3,3): **λ/16 ≈ 4,2 mm a 2,45 GHz**, **≈ 1,8 mm a 5,85 GHz**, **≈ 11,9 mm a 868 MHz** e **≈ 23,8 mm a 433 MHz**. Na prática toda trilha de 2,4/5 GHz até a antena ou o conector é linha de transmissão.
29. **Trilha de FR-4 longa é perda:** acima de "alguns centímetros", use conector e cabo coaxial. — FATO, NINA-B3 SIM.
30. **Pad mais largo que a linha** (pad de 0402, pad de conector): **abra o GND sob o pad** na camada de referência, para cortar a capacitância parasita. Em 2 camadas, com W de 0,9–1,0 mm, cada pad 0201/0402 já é uma descontinuidade; esse é um argumento a mais para 4 camadas. — FATO (para conector), NINA-B3 SIM; INFERÊNCIA (para o caso de 2 camadas).
31. **Folga trilha–GND lateral ≥ 2× a largura** quando a intenção é microstrip "guardada". — FATO, NINA-B3 SIM. *Nota:* a CPWG da Espressif usa gap ≈ W; é outra estrutura e foi calculada como tal. Não misture as duas regras.
32. **Calculadoras:**
    - JLCPCB Impedance Calculator: https://jlcpcb.com/pcb-impedance-calculator
    - Saturn PCB Toolkit: https://saturnpcb.com/saturn-pcb-toolkit/
    - Broadcom AppCAD (a Nordic recomenda): https://www.broadcom.com/info/wireless/appcad
    - KiCad PCB Calculator (aba Transmission Lines → "Coplanar wave guide with ground plane"): https://docs.kicad.org/9.0/en/pcb_calculator/pcb_calculator.html
    Use a da **fábrica como valor final**. — INFERÊNCIA quanto ao fluxo; URLs conferidas (HTTP 200).

### C. Redes de casamento

33. **Duas redes:** (a) **CLC/π colada no pino de RF do chip**, obrigatória para sintonia e supressão de harmônicas; (b) **CLC/π perto da antena**, recomendada, que pode ser dispensada se a simulação garantir 50 Ω. — FATO, Espressif C5 §1.3.6. TI: "it is recommended to add a pi-matching network so that the antenna can always be matched… one zero ohm resistor or DC block cap". — FATO, AN058 §3.4.
34. **Valores iniciais ESP32-C5** (tabela 4): **2,4 GHz:** C11 1,2–3,0 pF, L2 2,0–3,0 nH, C12 1,2–3,0 pF. **5 GHz:** C 0,2–1,5 pF, L 0–3 nH. Peças de exemplo: Murata **GRM0335C1H** (C0G, 0201) e **LQP03TN** (indutor de filme fino, 0201). **Critério de aceite** no VNA (porta 1 no lado do chip): S11 no **conjugado do chip, (40–45)+j0 Ω a 2,4 GHz e (50–65)+j0 Ω a 5 GHz**, e **S21 < −35 dB na 2ª e 3ª harmônicas**. — FATO, Espressif C5 §1.3.6.
35. **Os valores do módulo não se transferem para a sua placa:** "The RF matching parameters vary with the board". Afine na placa real. — FATO, Espressif C5.
36. **Tamanho e posição:**
    - componentes **0201**, colados no pino, em **zigue-zague** (os dois capacitores em direções diferentes);
    - **stub** no pad de GND do capacitor shunt do lado do chip, para atenuar a 2ª harmônica: comprimento **10 mil (C5)** ou **15 mil (C3/S3)**, impedância **100 Ω ±10 %**, referência em L3 com L2 aberto sob o stub;
    - **com 0402 ou maior, o stub não é necessário.**
    — FATO, Espressif C5/C3/S3 §1.4.4.
37. **ESD na antena:** a Espressif recomenda dispositivo de proteção ESD no caminho da antena (escolha de baixa capacitância é INFERÊNCIA). — FATO, Espressif C5/S3 §1.3.6.
38. **Dielétrico C0G/NP0 nos capacitores de RF** (estáveis com temperatura e tensão) e **indutores de filme fino ou de fio (wire-wound), de Q alto**, no caminho de RF. — INFERÊNCIA apoiada nas peças citadas pela Espressif (GRM03 C0G, LQP03) e nas curvas de dielétrico do u-blox UBX-15030289 §6.2.3. Indutor multicamada de ferrite comum não serve.
39. **Leitura do VNA:** VSWR **1,5 (RL 14 dB) é bom casamento**; VSWR **> 2,0 (RL 9,5 dB)** pede revisão. VSWR 2 é o limite usual para definir a banda. — FATO, TI AN058 §3.4. Na medição com cabo, fixe o cabo e use ferrite: placas pequenas têm muita corrente de modo comum. — FATO, AN058 §6. *Só mencionar:* medição em câmara e OTA ficam fora do escopo de layout.
40. **CC1101 (433/868):** use a rede do DN017 e do CC1101EM já salvos em `referencias\rf-reference-designs\cc1101-ti\`. Não duplicar aqui. — referência interna.
41. **Shunt mais perto do rádio aterrado no VSS mais próximo** (QFN). — FATO, Nordic DevZone nRF52.

### D. Vias de costura, cercas e blindagem

**Conta do passo de via (INFERÊNCIA; regra λ/10–λ/20 é prática comum, sem nota de fabricante que eu tenha lido):**
λ₀ = c/f; λg = λ₀/√εeff, com εeff ≈ 3,3 (conservador para linha externa em FR-4; na CPWG da tabela 1 o εeff é ~3,0–3,2, o que alongaria λg um pouco). Por exemplo, a 2,45 GHz: 299,79/2,45 = 122,4 mm → /√3,3 (1,817) = 67,4 mm → /20 = **3,37 mm**.

| f | λ₀ ar (mm) | λg εeff 3,3 (mm) | λg/10 | **λg/20** | λg/20 interno (εr 4,4) |
|---|---|---|---|---|---|
| 433,92 MHz | 690,9 | 380,3 | 38,0 | **19,0** | 16,5 |
| 868 MHz | 345,4 | 190,1 | 19,0 | **9,5** | 8,2 |
| 915 MHz | 327,6 | 180,4 | 18,0 | **9,0** | 7,8 |
| 1575,42 MHz (GPS L1) | 190,3 | 104,8 | 10,5 | **5,2** | 4,5 |
| 2,45 GHz | 122,4 | 67,4 | 6,7 | **3,4** | 2,9 |
| 5,5 GHz | 54,5 | 30,0 | 3,0 | **1,5** | 1,3 |
| 5,85 GHz | 51,2 | 28,2 | 2,8 | **1,4** | 1,2 |

42. **Passo da cerca ao longo da CPWG e das bordas:**
    - **≤ 3 mm** em placa só de 2,4 GHz;
    - **≤ 1,5 mm** onde passa 5 GHz (ESP32-C5);
    - **≤ 9 mm** em trecho só de 868/915 MHz.
    Dimensione pela **maior fundamental presente**, não pelas harmônicas (as harmônicas ficam com a rede e o filtro). — INFERÊNCIA (tabela acima). Dados primários disponíveis:
    - Nordic: "via **at least every 5 mm**" em áreas de GND (≈ λg/13 a 2,45 GHz) — FATO, página não mantida;
    - Silicon Labs: cerca "on both sides of a coplanar waveguide", sem passo — FATO;
    - RS9116 (Silicon Labs AN1341): costura de 32–100 mil — INFERÊNCIA, só vi em busca; documento exige login.
43. **Vias de GND junto a cada pad de GND** de componente de RF (no mínimo 2 por componente na Silicon Labs Z-Wave) **e dos dois lados do caminho de RF.** — FATO, Nordic DevZone; Silicon Labs Z-Wave 800 guide.
44. **Anel de GND na periferia de todas as camadas, costurado com o máximo de vias**, e **plano de alimentação recuado para dentro do contorno do GND**, para não formar antena de fenda na borda. O anel serve também de base para blindagem. — FATO, u-blox GNSS Antennas UBX-15030289 §6.2.1.
45. **Blindagem (shield can):** eficácia real de **30–40 dB** para lata metálica maciça (menos com cobre fino de PCB). **Furos e fendas longas reduzem a eficácia; fenda longa vira antena.** A tampa precisa fechar bem e ter boa ligação com a placa. — FATO, u-blox UBX-15030289 §6.3.
46. **Sinais que saem da lata:** filtre na passagem (feed-through). Na banda GNSS, **470 pF da série Murata NFM21C** ou, na falta dele, um **capacitor de 12 pF** junto à passagem. Também filtre DC. — FATO, u-blox UBX-15030289 §6.3.1.
47. **Fornecedores de lata SMT:**
    - **Würth WE-SHC**: peça única ou **moldura SMT/THT + tampa removível**, em fita e rolo para pick-and-place; aço estanhado de 0,2/0,3/0,5 mm ou latão de 0,15 mm; tamanhos-padrão de 3,1 × 3,1 até 60 × 60 mm, por exemplo 13,26 × 12,3 × 2,54 e 20 × 20 × 3. — FATO, catálogo: https://www.we-online.com/catalog/en/WE-SHC
    - **Clip WE-SHC 36900000**, para tampa removível. — INFERÊNCIA (busca).
    - "Até 60 dB de 500 MHz a 3 GHz" (Mouser) — INFERÊNCIA, não confirmado no datasheet.
    - Outros (Harwin EZ-BoardWare, Laird/DuPont, Masach) — INFERÊNCIA, não pesquisados a fundo.
    No footprint: **anel de pads ou trilha exposta com vias de GND em passo ≤ λg/20** da maior frequência dentro da lata. — INFERÊNCIA.

### E. Coexistência entre rádios e GNSS

48. **Isolamento necessário (Silicon Labs, FATO):** Wi-Fi a **+20 dBm, 100 % de duty cycle**, canal "far-away" e 20 MHz exige **50 dB** de isolamento entre antenas para receber BLE a −92 dBm, ou **45 dB** para 802.15.4 a −80 dBm. Wi-Fi a +10 dBm exige **≥ 40 dB** para receber 802.15.4 a −96 dBm. **Produtos pequenos costumam ter só 15–20 dB.** Canal "far-away" contra canal adjacente rende ~20 dB. — https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/04-managed-coexistence
49. **Quanto a distância rende (INFERÊNCIA, Friis, só campo distante, d > ~λ/2π, antenas isotrópicas):** FSPL = 20·log₁₀(4πd/λ). Para dois dipolos (2,15 dBi cada), subtraia ≈ 4,3 dB. Antenas no mesmo GND acoplam também por correntes no plano, então o isolamento real tende a ser **pior**.
    | f | λ/2π (limite) | d = 50 mm | d = 100 mm | d = 200 mm |
    |---|---|---|---|---|
    | 2,45 GHz | 19 mm | 14,2 dB | 20,2 dB | 26,3 dB |
    | 5,5 GHz | 9 mm | 21,2 dB | 27,3 dB | 33,3 dB |
    | 1575 MHz | 30 mm | 10,4 dB | 16,4 dB | 22,4 dB |
    | 868 MHz | 55 mm | (campo próximo) | 11,2 dB | 17,2 dB |
    **Conclusão:** em placa de ~100 mm, Wi-Fi e nRF24/BLE na mesma faixa têm ~16–20 dB, longe dos 40–50 dB. A solução tem de ser **no sistema** (TDM ou coexistência por GPIO, plano de canais, potência), não só no layout. — INFERÊNCIA consistente com a regra 48.
50. **Mais isolamento físico:** aumente a distância (potência ∝ 1/R² no campo distante) e use o nulo do monopolo. — FATO, Silicon Labs Unmanaged Coexistence. Trocar a posição das antenas por **bandas diferentes lado a lado** (por exemplo, sub-GHz ao lado de 2,4 GHz) e **bandas iguais nas pontas opostas** — INFERÊNCIA.
51. **ESP32-C5 com 2,4 e 5 GHz:** duas antenas separadas (ANT_2G/ANT_5G, multiplexadas no tempo, rede CLCCL em cada uma) **ou** uma antena dual-band via **diplexer LFD182G45DCHD481**. — FATO, Espressif C5 §1.3.6.
52. **GNSS, desempenho-alvo:** C/N₀ médio dos satélites altos **44–50 dBHz**; com antena ativa comum, **47 dBHz** deve sair fácil. — FATO, u-blox UBX-15030289 §2.1.
53. **GNSS, antena ativa ou passiva:**
    - antena **ativa** se o cabo passar de **~10 cm**;
    - LNA de **15 dB** basta até 5 m de cabo; não precisa passar de **26 dB**; **> 35 dB** com cabo curto pode saturar;
    - consumo da ativa: 3–20 mA, alimentada pelo coaxial (*bias tee*);
    - antena **passiva** exige microstrip ou stripline **≤ 10 cm** bem projetada.
    — FATO, u-blox UBX-15030289 §2.4 e tabela 1: https://content.u-blox.com/sites/default/files/products/documents/GNSS-Antennas_AppNote_%28UBX-15030289%29.pdf
54. **Antena GNSS:**
    - patch **25 × 25 mm** é o ótimo custo/desempenho; **< 17 × 17 mm** tem desempenho moderado;
    - GND de **50 × 50 a 70 × 70 mm** para patch;
    - **chip** e fractal **perdem 3 dB** por polarização linear e dependem muito do GND; distância de isolamento típica do chip **5 mm**;
    - no patch, nada de componentes ou sinais sob a antena ou perto dela, e distância mínima até a carcaça.
    — FATO, u-blox UBX-15030289 §3.1, §3.3, §5.1.
55. **GNSS junto de transmissor forte** (exemplo do documento: GSM): planeje **≥ 40 dB** de isolamento. Com ~20 dB obtidos só por posicionamento, é preciso **SAW na entrada GNSS**. — FATO, u-blox UBX-15030289 §5.4.1. O MAX-M10S já tem notch e SAW internos, e o manual sugere SAW externo em projetos com outros rádios: ver `referencias\rf-reference-designs\max-m10s-ublox\` (FATO, UBX-20053088 §RF front-end).
56. **Fontes de ruído para GNSS:** harmônicas de clock e de linhas digitais rápidas, SMPS e transmissores. **Planos sólidos (4 camadas)**, linhas rápidas curtas e terminadas, e **GND entre linhas em 2 camadas**. — FATO, u-blox UBX-15030289 §6.2 e white paper "GNSS interference": https://incremental-content.u-blox.com/sites/default/files/GNSS_Interference_white_paper_FINAL.PDF
57. **USB 3.x irradia ruído de banda larga em 2,4–2,5 GHz** (white paper da Intel, 2012). Mantenha conector, cabo e trilhas SuperSpeed longe de antenas de 2,4 GHz e GNSS. — INFERÊNCIA: a página da Intel bloqueou o acesso automático (403), e o conteúdo vem de resumos secundários. https://www.intel.com/content/www/us/en/content-details/841692/usb-3-0-radio-frequency-interference-impact-on-2-4-ghz-wireless-devices-white-paper.html
58. **SMPS longe do RF e o rádio no canto da placa**, longe de chaveamento. — FATO, Silicon Labs Z-Wave 800 guide ("close to a corner of the product's PCB, away from any high frequency switching circuits").

### F. Conectores RF

59. **SMA de borda (edge/end launch):**
    - GND interno **alinhado** com o GND do conector: um gap de 5 mil entre o plano e a borda já cria pico de impedância (perceptível perto de 25 GHz no estudo);
    - **pad do sinal estendido até a borda**;
    - **borda metalizada** (edge plating) melhora;
    - soldagem **com estêncil**: sem estêncil, o desempenho degradou muito;
    - todos os contatos de GND soldados.
    — FATO, Stavoli/Correia/Soubh, Signal Integrity Journal, 2019: https://www.signalintegrityjournal.com/articles/1094-demystifying-edge-launch-connectors. Em 2,4–6 GHz essas descontinuidades pesam bem menos que em 25 GHz — INFERÊNCIA.
60. **Espessura:** o edge SMA é especificado por espessura de placa (famílias para 0,062" = 1,57 mm são as comuns). Confirme no datasheet do PN escolhido na LCSC. — INFERÊNCIA (busca: Amphenol 132289/132384 "for 0.062 inch PCB").
61. **SMA PTH:** GND aberto em todas as camadas em volta do pino central, até os anéis dos 4 postes de GND. **u.FL:** nada de cobre condutor sob o conector, entre os pads de GND, e GND aberto sob o pad ativo pelo menos na 1ª camada interna. — FATO, NINA-B3 SIM. Espressif: "keep all layers clear under the IPEX antenna connector". — FATO, C5 §1.4.4.
62. **u.FL é para poucos ciclos.** O valor usual é **~30 acoplamentos** e **altura acoplada ≤ 2,5 mm** (INFERÊNCIA: listagens de distribuidor e página Hirose via busca, porque o site da Hirose bloqueou o acesso; confirme no PN). Para robustez, leve o u.FL a um **SMA de painel por pigtail**. Cabos de **0,8–1,37 mm**, comprimentos padrão de **100/200 mm**. — FATO, NINA-B3 SIM. **MHF4** (I-PEX) é a geração menor, usada em módulos M.2; confira altura e ciclos no datasheet — INFERÊNCIA.
63. **Em produto Wi-Fi/BT, o padrão de fato é RP-SMA**, para dificultar a troca por antena de ganho maior e o estouro do limite regulatório de EIRP. — FATO, NINA-B3 SIM.
64. **Pigtail u.FL→SMA:** raio de curvatura adequado, conector do módulo virado para a saída, cabo fixo. — INFERÊNCIA, já é regra da casa (§14).

### G. Conformidade (RED/CE) e pré-certificação

65. **Módulo certificado contra chip discreto.** O ETSI EG 203 367 permite **reaproveitar a avaliação já feita no módulo**, tanto de EMC (art. 3.1b, §5) quanto de **espectro (art. 3.2, §6)**, se o módulo for instalado em **condições equivalentes** às da avaliação original e **conforme as instruções de instalação do módulo**. Pontos importantes:
    - Se as condições divergirem, ou se o fabricante do produto **alterar qualquer aspecto do projeto ou do layout físico** do rádio original, é preciso reavaliar o art. 3.2 com as normas de rádio.
    - Em **multirrádio com mais de um transmissor ao mesmo tempo**, reavaliar **espúrios e intermodulação**.
    - Para EMC, se rádio e não-rádio operam juntos, é preciso reavaliar pelo EN 301 489-x.
    — FATO, ETSI EG 203 367 V1.1.1 §5.1.1.2, §6.1 e §6.2: https://www.etsi.org/deliver/etsi_eg/203300_203399/203367/01.01.01_60/eg_203367v010101p.pdf
66. **Consequência no layout:** com módulo, **não altere o caminho de RF certificado**. Respeite keepout e carcaça, use **só antenas da lista certificada do módulo** (mesmo tipo, ganho ≤) e **não ponha amplificador nem atenuador**. Antena diferente, cabo, SMA trocável ou ganho maior podem quebrar as "condições equivalentes" e exigir ensaio de rádio completo. Dois ESP32-C5 transmitindo ao mesmo tempo (ou ESP + CC1101 + nRF24) caem na regra de espúrios e intermodulação da §6.2. — FATO quanto à §6.2; o resto é INFERÊNCIA (aplicação do EG 203 367 e da regra 63).
67. **Chip discreto (CC1101, nRF24, ESP32-C5 nu):** o produto final faz **todos os ensaios de rádio** do art. 3.2. Normas típicas, a confirmar com o laboratório e na lista vigente da Decisão de Execução (UE) 2022/2191 consolidada (https://eur-lex.europa.eu/eli/dec_impl/2022/2191/oj):
    - **EN 300 328** (2,4 GHz), confirmado na lista em busca;
    - **EN 300 220-2** (SRD 25–1000 MHz, CC1101), confirmado na lista em busca;
    - **EN 301 893** (RLAN de 5 GHz), não confirmado;
    - **EN 303 413** (receptores GNSS), não confirmado;
    - **EN 301 489-1/-17** (EMC), não confirmado;
    - exposição RF (EN 62479/EN 62311).
    O ESP32-C5 nu também exige firmware de teste de RF (a Espressif pede manter a UART de download para isso). — FATO quanto à UART, C5 §1.5 (Download Guidelines); o resto é INFERÊNCIA.
68. **Cibersegurança RED:** o Regulamento Delegado (UE) 2022/30 (art. 3.3 d/e/f) vale para rádios conectados desde **1º/08/2025**, com as normas harmonizadas EN 18031-1/-2/-3 (com restrições). Não afeta o layout, mas afeta o produto. — INFERÊNCIA: URL do EUR-Lex conferida (200), texto não lido nesta pesquisa; https://eur-lex.europa.eu/eli/reg_del/2022/30/oj
69. **Pré-certificação barata:** prever **conector de teste ou ponto para coaxial** (pad para u.FL não montado, ou π com 0 Ω que permite desviar para conector) para medir potência e harmônicas conduzidas antes do laboratório. — INFERÊNCIA (prática comum).

---

## Erros comuns

| Erro | Consequência | Correção |
|---|---|---|
| Módulo com antena impressa no meio da placa, ou GND/trilhas sob a antena | Antena desintonizada, alcance cai muito | Antena para fora da borda ou base cortada sob a antena e dos lados; keepout em todas as camadas (Espressif, TI AN058) |
| Recorte de GND sob a antena feito em módulo que pede GND cheio (ex.: NINA-B3x2), ou o contrário | Desempenho abaixo do datasheet | Ler o keepout do PN exato (NINA-B3 SIM) |
| Carcaça, bateria ou parafuso a < 10–15 mm da antena | Deslocamento de ressonância e perda de eficiência | ≥ 15 mm (Espressif) ou ≥ 10 mm de metal e ≥ 5–10 mm de carcaça (NINA-B3); afinar a π dentro da carcaça |
| "50 Ω de olho" em 2 camadas com microstrip de 0,3 mm | Z real ≫ 50 Ω (a 1,6 mm precisa de 2,8 mm) | CPWG calculada, ou 4 camadas com impedância controlada da JLC |
| CPWG em 2 camadas com gap pequeno (0,15 mm) | ±0,05 mm de corrosão leva a ±6 Ω | Gap ≥ 0,2–0,25 mm com W correspondente, ou 4 camadas |
| Usar a largura de outra fábrica ou outro stackup | Descasamento | Recalcular no `JLC04161H-7628` (W ≈ 0,30 / gap 0,30 mm) e confirmar na calculadora da JLC |
| Trilha de RF trocando de camada por via ou ramificada (stub) | Reflexão, ressonância, perda | Só na camada externa, sem vias, sem ramos (Espressif) |
| Copiar os valores da rede do módulo ou do eval board | Casamento errado, harmônicas acima do limite | Footprint de π/CLC e sintonia com VNA na placa real (Espressif, TI) |
| Sem footprint de π perto da antena | Impossível corrigir a desintonia da carcaça sem nova placa | π com 0 Ω/DNP de fábrica (TI AN058, DN023) |
| Capacitor X7R ou indutor de ferrite multicamada na rede de RF | Q baixo, deriva | C0G e filme fino/wire-wound (peças Espressif) |
| Vias de costura espaçadas por regra de olho (10 mm) em 5 GHz | Fuga e acoplamento entre canais | Passo ≤ 1,5 mm em 5 GHz, ≤ 3 mm em 2,4 GHz (tabela D) |
| Achar que 2 cm de distância isolam Wi-Fi de nRF24 | Dessensibilização de 20–30 dB | Plano de canais, TDM e coexistência; afastar ao máximo; nulo do monopolo (Silicon Labs) |
| SMA espaçados ~18 mm com antenas da mesma banda | Antenas no campo próximo (λ/2π = 19,5 mm a 2,45 GHz), isolamento baixo | Bandas diferentes lado a lado; bandas iguais nas pontas |
| GNSS perto de SMPS, USB 3 ou cristal, sem SAW | C/N₀ baixo, perda de fix | Afastar, SAW, blindar a fonte de ruído (u-blox) |
| Shield can com fenda longa ou poucos pontos de solda | Lata irradia como antena de fenda | Moldura contínua, vias densas, tampa bem fechada (u-blox) |
| Edge SMA com plano interno recuado da borda ou sem estêncil | Pico de impedância e degradação | GND até a borda, pad até a borda, estêncil (SIJ) |
| Trocar a antena do módulo por outra fora da lista certificada | Perde o reaproveitamento da avaliação RED | Usar antena da lista; senão, ensaio de rádio completo (EG 203 367) |
| Vários transmissores ligados ao mesmo tempo sem avaliar a combinação | Espúrios e intermodulação fora do limite | Reavaliar espúrios e intermodulação do conjunto (EG 203 367 §6.2) |

---

## Checklist

**Arquitetura**
- [ ] Rádio = módulo certificado sempre que possível; anotar o PN e a lista de antenas certificadas.
- [ ] 4 camadas (`JLC04161H-7628`) se houver trilha de RF de 50 Ω até antena ou conector; impedância controlada pedida no pedido da JLC.
- [ ] Rádios da mesma faixa com estratégia de coexistência definida (TDM/GPIO/canais), além do layout.

**Antena**
- [ ] Keepout do datasheet do PN exato aplicado em **todas as camadas** (zona de keepout no KiCad: sem cobre, sem trilhas, sem vias, sem pads).
- [ ] Antena impressa do módulo fora da borda, ou base cortada sob a antena e dos lados (nunca recorte nos 4 lados).
- [ ] Folga até a carcaça: ≥ 15 mm (ESP), ou ≥ 5–10 mm (NINA-B3); metal e bateria ≥ 10–15 mm.
- [ ] Plano de GND ≥ λ/4 da menor frequência (31 mm a 2,4 GHz; 86 mm a 868 MHz) ou antena externa.
- [ ] Antena de PCB copiada do DXF/Gerber de referência, na mesma espessura e no mesmo material.
- [ ] Antena chip na borda, com as folgas do fabricante (Johanson > 2 mm/> 4 mm; AVX com feed a 5–15 mm do canto).
- [ ] USB, UART, cristal, clocks e SMPS longe da antena.

**Linha de transmissão**
- [ ] Largura e gap da CPWG calculados no stackup real (W ≈ 0,30 / gap 0,30 mm no JLC04161H-7628) e conferidos na calculadora da JLC.
- [ ] L2 GND sólido sob toda a trilha; nada roteado sob ela.
- [ ] Trilha só em L1, sem vias, sem ramos, curvas a 135° ou em arco, largura constante.
- [ ] GND aberto sob pads mais largos que a linha (pad de conector).
- [ ] Netclass "RF_50R" no KiCad com W/gap fixos; conferir depois do roteamento (o Freerouting não pode tocar no RF).

**Casamento**
- [ ] π/CLC colada no pino do rádio (0201, ou 0402 C0G), capacitores em zigue-zague, shunt aterrado no VSS mais próximo.
- [ ] Stub de 2ª harmônica (10–15 mil, 100 Ω) se usar 0201 no ESP32; dispensável em 0402.
- [ ] π perto da antena ou do conector, montada com 0 Ω/DNP.
- [ ] ESD de baixa capacitância no caminho da antena (Espressif).
- [ ] Plano de sintonia com VNA: S11 alvo (40–45)+j0 Ω a 2,4 GHz e (50–65)+j0 Ω a 5 GHz no ESP32-C5; S21 < −35 dB nas harmônicas.

**Vias e blindagem**
- [ ] Cerca de vias dos dois lados da CPWG, com passo ≤ 3 mm (2,4 GHz) / ≤ 1,5 mm (5 GHz) / ≤ 9 mm (sub-GHz).
- [ ] Vias de GND junto a cada pad de GND de RF (≥ 2 por componente).
- [ ] Anel de GND costurado na periferia; planos de alimentação recuados do contorno do GND.
- [ ] Shield can SMT (moldura + tampa) sobre rádio nu, com footprint de anel e vias densas; filtrar os sinais que entram e saem.

**GNSS**
- [ ] Antena passiva: trilha ≤ 10 cm; ativa: bias tee e LNA de 15–26 dB.
- [ ] SAW na entrada se houver transmissor forte na placa; GNSS longe de SMPS e USB 3.
- [ ] Patch 25 × 25 mm com GND de 50–70 mm, ou chip com o GND exigido.

**Conectores**
- [ ] Edge SMA na variante da espessura da placa (1,6 mm), GND alinhado até a borda, pad até a borda.
- [ ] u.FL com cobre aberto sob o conector; pigtail com raio de curvatura adequado.
- [ ] RP-SMA em produto Wi-Fi/BT (ou justificar SMA).

**Conformidade**
- [ ] Caminho de RF do módulo intacto, antena da lista certificada e manual de instalação do módulo seguido (EG 203 367).
- [ ] Chip discreto: orçamento de ensaio de rádio completo (EN 300 328 / 300 220-2 / 301 893…) e firmware de teste.
- [ ] Ponto de teste conduzido (u.FL DNP ou π) para pré-certificação.

---

## Conflitos com PADROES-PROJETO-PCB.md

| § PADROES | Regra da casa | Literatura | Situação |
|---|---|---|---|
| §1 | 4 camadas sempre que houver RF "que precisa funcionar de verdade"; stackup `JLC04161H-7628` | A JLC lista impedância controlada a partir de 4 camadas; 2 camadas não consta (FATO, conferido 2026-11-20). Espressif e Nordic aceitam 2 camadas com GND sólido e CPWG (FATO). | **Confirma** para a JLC; a literatura admite 2 camadas, mas sem impedância testada. |
| §3 | "Impedância 50 Ω controlada (microstrip… exige 4 camadas)" | É possível em 2 camadas com CPWG (Tabela 2), mas com sensibilidade alta ao gap. | **Diverge parcialmente:** "exige" vale para impedância **testada** na JLC, não para a física. |
| §3 contra §14 | §3 diz "microstrip"; §14 diz "CPWG 50 Ω" | Silicon Labs e Nordic recomendam CPWG; a Espressif usa CPWG. | **Contradição interna** do PADROES: sugerir unificar em "CPWG sobre L2". |
| §3 | Rádios da mesma faixa separados ao longo da borda | Separar é correto, mas o espaço físico dá ~15–20 dB contra 40–50 dB necessários (Silicon Labs). | **Confirma, mas falta:** coexistência no sistema (TDM/GPIO, plano de canais, potência). |
| §3 | Rede de casamento "oficial do fabricante, nunca inventar" | A Espressif diz que os valores do módulo **não se transferem**; afinar com VNA na placa real. TI: π sempre, com 0 Ω se já casado. | **Diverge parcialmente / falta:** footprint de π na antena ou conector, e plano de sintonia com VNA. |
| §3 / §14 | (não fala do tamanho dos componentes de RF) | Espressif: 0201 + stub de harmônica; com 0402 dispensa o stub. | **Falta.** |
| §3 | (não fala de ESD na antena) | Espressif recomenda ESD no caminho da antena. | **Falta.** |
| §3 | (não fala de keepout de módulo com antena impressa nem de folga até a carcaça) | Espressif: ≥ 15 mm até a carcaça, base cortada; NINA-B3: canto/borda, metal ≥ 10 mm. | **Falta.** |
| §3 | Shield can sobre chip nu, moldura soldável + tampa, anel de vias | u-blox: lata dá 30–40 dB; fendas e furos degradam; anel de GND costurado; filtrar as passagens. Würth WE-SHC tem moldura SMT + tampa. | **Confirma** (acrescentar: filtros de passagem e passo das vias pela tabela D). |
| §3 | Antena GPS ativa → bias tee | u-blox: ativa se cabo > 10 cm; LNA de 15–26 dB; 3–20 mA pelo coaxial. | **Confirma** (acrescentar os limites de ganho do LNA). |
| §4 | ~18 mm entre centros de SMA | A 2,45 GHz, λ/2π ≈ 19,5 mm, então antenas da mesma banda a 18 mm estão no campo próximo. Nenhuma fonte apoia esse valor para a mesma banda. | **Diverge:** manter 18 mm só entre bandas diferentes, e afastar ao máximo as da mesma banda. |
| §4 | SMA fêmea edge-mount 50 Ω como padrão | NINA-B3: o padrão de fato em Wi-Fi/BT é **RP-SMA** (anti-troca por antena de ganho maior). EG 203 367: antena trocável pode tirar o produto das "condições equivalentes" do módulo. | **Falta:** decidir SMA ou RP-SMA por produto e checar a lista de antenas certificadas do módulo. |
| §4 | Atenção à espessura do edge SMA (1,6 mm) | As famílias "for 0.062 in PCB" confirmam; SIJ: GND interno alinhado, pad até a borda, estêncil. | **Confirma** (acrescentar os detalhes de transição). |
| §14 | Rede compacta colada ao pino, saída única em CPWG até o SMA | Espressif: CLC colada, zigue-zague, trilha sem vias nem ramos, 135°. | **Confirma.** |
| §14 | Cercas de via separando domínios de RF | Silicon Labs: cerca dos dois lados da CPW. Passo: tabela D (≤ 1,5 mm em 5 GHz). | **Confirma** (falta o número do passo). |
| §14 | u.FL virado para a antena, com raio de curvatura do pigtail | NINA-B3: u.FL com poucos ciclos, levar a SMA de painel; cobre aberto sob o u.FL. | **Confirma** (acrescentar o keepout de cobre sob o u.FL). |
| §14 | SMPS longe do RF, num canto | Silicon Labs: rádio no canto, longe do chaveamento; u-blox: SMPS é fonte de ruído GNSS. | **Confirma.** |

---

## Bibliografia

**Livros** (só citar; não baixar)
- Bowick, C.; Ajluni, C.; Blyler, J. *RF Circuit Design*, 2ª ed., Newnes/Elsevier, 2008. Redes de casamento L/π/T e Smith chart, de forma prática. Base para entender a π da Espressif e da TI.
- Pozar, D. M. *Microwave Engineering*, 4ª ed., Wiley, 2011. Linhas de transmissão (microstrip, CPW), casamento e S-parameters; referência acadêmica padrão.
- Balanis, C. A. *Antenna Theory: Analysis and Design*, 4ª ed., Wiley, 2016. Teoria de monopolo/IFA, campo próximo e distante, polarização.
- Wadell, B. C. *Transmission Line Design Handbook*, Artech House, 1991. Fórmulas fechadas de CPWG e microstrip usadas na memória de cálculo.
- **Correção do brief:** "Trilogy of Wireless" da Würth é *Trilogy of Wireless Power Transfer* (transferência de energia sem fio), **não** trata de antenas de comunicação. Não incluído como fonte. https://www.we-online.com/catalog/en/TRILOGY_WIRELESSPOWER

**Normas** (só citar)
- IPC-2141A, *Design Guide for High-Speed Controlled Impedance Circuit Boards*. Não lido; norma paga.
- ETSI EN 300 328 (2,4 GHz), EN 300 220-2 (SRD sub-GHz), EN 301 893 (5 GHz RLAN), EN 303 413 (GNSS), EN 301 489-1/-17 (EMC rádio): https://www.etsi.org/standards (gratuitas no site do ETSI; não baixadas, porque são grandes e o tema principal é layout).
- Diretiva RED 2014/53/UE: https://eur-lex.europa.eu/eli/dir/2014/53/oj · Regulamento Delegado (UE) 2022/30: https://eur-lex.europa.eu/eli/reg_del/2022/30/oj · Lista de normas harmonizadas, Decisão de Execução (UE) 2022/2191 (consolidada): https://eur-lex.europa.eu/eli/dec_impl/2022/2191/oj

**App notes e guias de fabricante** (baixados em `pdfs\03-rf\`, salvo indicação)
- Espressif, *ESP32-C5 / ESP32-S3 / ESP32-C3 Hardware Design Guidelines* (release master, baixados em 2026-11-20). https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/esp-hardware-design-guidelines-en-master-esp32c5.pdf (trocar `esp32c5` por `esp32s3`/`esp32c3`). Fonte principal de módulo, stackup, π, stub e keepout.
- TI AN058 *Antenna Selection Guide* (SWRA161B): https://www.ti.com/lit/an/swra161b/swra161b.pdf
- TI DN007 *2.4-GHz Inverted F Antenna* (SWRU120D): https://www.ti.com/lit/an/swru120d/swru120d.pdf
- TI AN043 *Small Size 2.4 GHz PCB antenna* (SWRA117D): https://www.ti.com/lit/an/swra117d/swra117d.pdf
- TI DN023 *868/915/955 MHz Inverted F Antenna* (SWRA228C): https://www.ti.com/lit/an/swra228c/swra228c.pdf
- TI AN074 *RemoTI Coexistence Testing* (SWRA285): https://www.ti.com/lit/an/swra285/swra285.pdf. Coexistência 802.15.4 × Wi-Fi em nível de protocolo; pouco valor para layout.
- u-blox *GNSS Antennas — RF design considerations* UBX-15030289 R03: https://content.u-blox.com/sites/default/files/products/documents/GNSS-Antennas_AppNote_%28UBX-15030289%29.pdf
- u-blox *GNSS interference* white paper: https://incremental-content.u-blox.com/sites/default/files/GNSS_Interference_white_paper_FINAL.PDF
- u-blox *NINA-B3 System Integration Manual* UBX-17056748 R15 (módulo nRF52840): https://content.u-blox.com/sites/default/files/NINA-B3_SIM_UBX-17056748.pdf
- Johanson Technology, *Chip Antenna Layout Considerations for 802.11 Applications* (2006): https://johansontechnology.com/docs/2/jti-antenna-mounting.pdf
- Kyocera AVX, *AppNote 1001013 Wi-Fi/Bluetooth PCB Antenna (On/Off Ground)*: https://www.kyocera-avx.com/docs/techinfo/ApplicationNotes/Antenna-AppNotes/AVX-E_AppNote-1001013.pdf
- ETSI EG 203 367 V1.1.1 (2016), RED para equipamentos multirrádio e combinados (módulos): https://www.etsi.org/deliver/etsi_eg/203300_203399/203367/01.01.01_60/eg_203367v010101p.pdf
- Já no acervo (não duplicado): TI DN017 e CC1101EM 434 MHz (`rf-reference-designs\cc1101-ti\`), u-blox MAX-M10S Integration Manual UBX-20053088 (`rf-reference-designs\max-m10s-ublox\`), Nordic nRF24L01 Product Spec v2.0 (`rf-reference-designs\nrf24l01-nordic\`).

**Fontes lidas on-line (não baixáveis ou HTML)**
- Silicon Labs, *Managed Coexistence* e *Unmanaged Coexistence*: https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/04-managed-coexistence · https://docs.silabs.com/coexistence/latest/multiprotocol-wifi-coexistence-fundamentals/03-unmanaged-coexistence
- Silicon Labs, *Z-Wave 800 Series Integration Guide — PCB Implementation*: https://docs.silabs.com/z-wave/8.0.0/z-wave-800-series-integration-guide/08-pcb-implementation
- Nordic DevZone, *General PCB design guidelines for nRF52 series* (página não mantida): https://devzone.nordicsemi.com/guides/hardware-design-test-and-measuring/b/nrf5x/posts/general-pcb-design-guidelines-for-nrf52-series
- Microchip, BM20/23 *Module Placement Rules*: https://onlinedocs.microchip.com/oxy/GUID-26060FFF-4EA0-483D-BCBB-39AF46A5A76C-en-US-6/GUID-3351AEE9-DDD5-4583-8492-53634B5FD77C.html
- Stavoli, Correia, Soubh, *Demystifying Edge Launch Connectors*, Signal Integrity Journal, 2019: https://www.signalintegrityjournal.com/articles/1094-demystifying-edge-launch-connectors
- JLCPCB: stackups de impedância https://jlcpcb.com/impedance · capacidades https://jlcpcb.com/capabilities/Capabilities · exemplo de calculadora (pergunta de usuário) https://jlcpcb.com/help/answers/detail/331-Coplanar-and-non-coplanar-Impedance-calculator
- Würth WE-SHC (catálogo): https://www.we-online.com/catalog/en/WE-SHC
- Espressif, certificados dos módulos (CE/RED, FCC etc.): https://www.espressif.com/en/support/documents/certificates

**Pedidas no brief, mas não acessíveis em 2026-11-20** (bloqueio a cliente automatizado; existem, conforme busca)
- Silicon Labs AN1088 *Designing with an Inverted-F 2.4 GHz PCB Antenna*: https://www.silabs.com/documents/public/application-notes/an1088-designing-with-pcb-antenna.pdf (403)
- Silicon Labs AN928.2 *EFR32 Series 2 Layout Design Guide*: https://www.silabs.com/documents/public/application-notes/an928.2-efr32-series2-layout-design-guide.pdf (403)
- Nordic nWP-017 *Antenna tuning* (v1.0, 2012) e nWP-008 *λ/4 printed monopole 2.45 GHz*: https://docs.nordicsemi.com/bundle/nwp_017/resource/nwp_017.pdf (Cloudflare); o endereço antigo infocenter redireciona para a página inicial.
- **AN2731 não é da Microchip:** é a *Compact Planar Antennas for 2.4 GHz Communication* da **NXP (ex-Freescale)**, Rev. 4, 11/2020. O link nxp.com (https://www.nxp.com/docs/en/application-note/AN2731.pdf) deu 404; espelhos não oficiais não foram usados.
- Würth ANR017 *GNSS Antenna Selection* (403); Ignion manuais mXTEND (Mouser 403); Hirose U.FL (403); Intel USB 3.0 RFI white paper (403).

**Ferramentas e calculadoras**
- JLCPCB Impedance Calculator: https://jlcpcb.com/pcb-impedance-calculator
- Saturn PCB Toolkit: https://saturnpcb.com/saturn-pcb-toolkit/
- Broadcom AppCAD: https://www.broadcom.com/info/wireless/appcad
- KiCad PCB Calculator (Transmission Lines): https://docs.kicad.org/9.0/en/pcb_calculator/pcb_calculator.html
- Cursos e vídeos: não pesquisados nesta rodada (lacuna).
